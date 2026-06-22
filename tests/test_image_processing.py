import unittest
from PIL import Image
from utils.image_processing import apply_filter

class TestImageProcessing(unittest.TestCase):
    def setUp(self):
        # Create a basic red 100x100 RGB image for testing
        self.test_image = Image.new("RGB", (100, 100), color=(255, 0, 0))

    def test_apply_filter_bw(self):
        img = apply_filter(self.test_image, 'filter_bw')
        self.assertEqual(img.mode, 'L')

    def test_apply_filter_sepia(self):
        img = apply_filter(self.test_image, 'filter_sepia')
        self.assertEqual(img.mode, 'RGB')
        # Ensure it actually ran and modified pixels (red should become sepia-toned)
        r, g, b = img.getpixel((50, 50))
        # Warm sepia should have reduced red and added green/blue ratio
        self.assertNotEqual((r, g, b), (255, 0, 0))

    def test_apply_filter_contrast(self):
        img = apply_filter(self.test_image, 'filter_contrast')
        self.assertEqual(img.mode, 'RGB')

    def test_apply_filter_sharpen(self):
        img = apply_filter(self.test_image, 'filter_sharpen')
        self.assertEqual(img.mode, 'RGB')

    def test_apply_filter_blur(self):
        img = apply_filter(self.test_image, 'filter_blur')
        self.assertEqual(img.mode, 'RGB')

    def test_apply_filter_grayscale(self):
        img = apply_filter(self.test_image, 'filter_grayscale')
        self.assertEqual(img.mode, 'L')

    def test_apply_filter_invert(self):
        img = apply_filter(self.test_image, 'filter_invert')
        self.assertEqual(img.mode, 'RGB')
        # Inverse of pure red (255,0,0) is cyan (0,255,255)
        self.assertEqual(img.getpixel((50, 50)), (0, 255, 255))

    def test_apply_filter_contour(self):
        img = apply_filter(self.test_image, 'filter_contour')
        self.assertEqual(img.mode, 'RGB')

    def test_apply_filter_emboss(self):
        img = apply_filter(self.test_image, 'filter_emboss')
        self.assertEqual(img.mode, 'RGB')

    def test_apply_filter_detail(self):
        img = apply_filter(self.test_image, 'filter_detail')
        self.assertEqual(img.mode, 'RGB')

    def test_apply_filter_brightness(self):
        img = apply_filter(self.test_image, 'filter_brightness')
        self.assertEqual(img.mode, 'RGB')

    def test_apply_filter_warm(self):
        img = apply_filter(self.test_image, 'filter_warm')
        self.assertEqual(img.mode, 'RGB')

    def test_apply_filter_cool(self):
        img = apply_filter(self.test_image, 'filter_cool')
        self.assertEqual(img.mode, 'RGB')

    def test_apply_filter_invalid(self):
        # Invalid filter should return image unchanged
        img = apply_filter(self.test_image, 'invalid_filter_name')
        self.assertEqual(img, self.test_image)

if __name__ == '__main__':
    unittest.main()
