import numpy as np
import cv2
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

try:
    from pyzbar.pyzbar import decode as _zbar_decode
except Exception:
    _zbar_decode = None


def _pil_to_cv(image: Image.Image) -> np.ndarray:
    arr = np.array(image.convert('RGB'))
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)


def _cv_to_pil(mat: np.ndarray) -> Image.Image:
    if len(mat.shape) == 2:
        return Image.fromarray(mat)
    return Image.fromarray(cv2.cvtColor(mat, cv2.COLOR_BGR2RGB))


def _order_points(pts: np.ndarray) -> np.ndarray:
    """Order 4 points as top-left, top-right, bottom-right, bottom-left."""
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def _find_document_contour(image: np.ndarray):
    """Try to find a 4-point contour resembling a paper sheet."""
    h, w = image.shape[:2]
    ratio = 800.0 / max(h, w)
    small = cv2.resize(image, (int(w * ratio), int(h * ratio)))

    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)
    edged = cv2.dilate(edged, np.ones((3, 3), np.uint8), iterations=1)

    contours, _ = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

    img_area = small.shape[0] * small.shape[1]
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4 and cv2.contourArea(approx) > img_area * 0.2:
            return approx.reshape(4, 2) / ratio
    return None


def auto_crop_and_warp(image: Image.Image) -> Image.Image:
    """
    Detect document edges and apply perspective transform to flatten the page.
    Returns the original image if no plausible quadrilateral is found.
    """
    cv_img = _pil_to_cv(image)
    quad = _find_document_contour(cv_img)
    if quad is None:
        return image

    rect = _order_points(quad)
    (tl, tr, br, bl) = rect
    width_a = np.linalg.norm(br - bl)
    width_b = np.linalg.norm(tr - tl)
    max_w = int(max(width_a, width_b))
    height_a = np.linalg.norm(tr - br)
    height_b = np.linalg.norm(tl - bl)
    max_h = int(max(height_a, height_b))

    if max_w < 50 or max_h < 50:
        return image

    dst = np.array([
        [0, 0],
        [max_w - 1, 0],
        [max_w - 1, max_h - 1],
        [0, max_h - 1]
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(cv_img, M, (max_w, max_h))
    return _cv_to_pil(warped)


def adaptive_bw(image: Image.Image) -> Image.Image:
    """Clean B/W using adaptive threshold — flattens lighting, removes background."""
    cv_img = _pil_to_cv(image)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    bw = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 15
    )
    return _cv_to_pil(bw)


def boost_contrast(image: Image.Image) -> Image.Image:
    """CLAHE — local contrast enhancement that preserves color."""
    cv_img = _pil_to_cv(image)
    lab = cv2.cvtColor(cv_img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    l = clahe.apply(l)
    merged = cv2.merge((l, a, b))
    return _cv_to_pil(cv2.cvtColor(merged, cv2.COLOR_LAB2BGR))


def scan_qr_codes(image: Image.Image) -> list[str]:
    """Return decoded payloads of every QR / barcode found in the image."""
    if _zbar_decode is None:
        return []
    try:
        results = _zbar_decode(image.convert('RGB'))
    except Exception:
        return []
    out = []
    for r in results:
        try:
            out.append(r.data.decode('utf-8', errors='replace'))
        except Exception:
            continue
    return out


def apply_filter(image: Image.Image, filter_type: str) -> Image.Image:
    """
    Applies a specified filter to a PIL Image and returns the modified image.
    """
    if filter_type == 'filter_bw':
        return image.convert('L')
    elif filter_type == 'filter_sepia':
        matrix = (
            0.393, 0.769, 0.189, 0,
            0.349, 0.686, 0.168, 0,
            0.272, 0.534, 0.131, 0
        )
        return image.convert('RGB').convert('RGB', matrix)
    elif filter_type == 'filter_contrast':
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(2.0)
    elif filter_type == 'filter_sharpen':
        return image.filter(ImageFilter.SHARPEN)
    elif filter_type == 'filter_blur':
        return image.filter(ImageFilter.BLUR)
    elif filter_type == 'filter_grayscale':
        return image.convert('L')
    elif filter_type == 'filter_invert':
        return ImageOps.invert(image.convert('RGB'))
    elif filter_type == 'filter_contour':
        return image.filter(ImageFilter.CONTOUR)
    elif filter_type == 'filter_emboss':
        return image.filter(ImageFilter.EMBOSS)
    elif filter_type == 'filter_detail':
        return image.filter(ImageFilter.DETAIL)
    elif filter_type == 'filter_brightness':
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(1.5)
    elif filter_type == 'filter_warm':
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(1.5)
    elif filter_type == 'filter_cool':
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(0.5)
    elif filter_type == 'filter_scan_bw':
        return adaptive_bw(image)
    elif filter_type == 'filter_scan_color':
        return boost_contrast(image)
    else:
        return image


def process_image(
    image_path: str,
    filter_type: str,
    auto_crop: bool = True,
) -> Image.Image:
    """
    Opens an image, fixes EXIF orientation, optionally auto-crops & flattens
    the document, applies the chosen filter, and returns the result.
    """
    with Image.open(image_path) as img:
        img = ImageOps.exif_transpose(img)
        img.load()

    if auto_crop:
        try:
            img = auto_crop_and_warp(img)
        except Exception:
            pass

    img = apply_filter(img, filter_type)
    img.load()
    return img
