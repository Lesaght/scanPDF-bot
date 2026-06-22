import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from docx import Document


def _register_unicode_font():
    """Register a Unicode TTF font for Cyrillic support; fallback to Helvetica."""
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if os.path.exists(path) and path.endswith(".ttf"):
            try:
                pdfmetrics.registerFont(TTFont("DocFont", path))
                return "DocFont"
            except Exception:
                continue
    return "Helvetica"


def text_to_pdf(text: str, output_path: str) -> None:
    font_name = _register_unicode_font()
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
    )
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = font_name
    style.fontSize = 12
    style.leading = 16

    story = []
    for line in text.split("\n"):
        safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        if safe.strip() == "":
            story.append(Spacer(1, 12))
        else:
            story.append(Paragraph(safe, style))
    doc.build(story)


def text_to_docx(text: str, output_path: str) -> None:
    document = Document()
    for line in text.split("\n"):
        document.add_paragraph(line)
    document.save(output_path)


def text_to_txt(text: str, output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)


def generate_document(text: str, fmt: str, output_dir: str) -> tuple[str, str]:
    """Generate a document in the requested format. Returns (path, filename)."""
    fmt = (fmt or "pdf").lower()
    if fmt == "docx":
        path = os.path.join(output_dir, "document.docx")
        text_to_docx(text, path)
        return path, "document.docx"
    if fmt == "txt":
        path = os.path.join(output_dir, "document.txt")
        text_to_txt(text, path)
        return path, "document.txt"
    path = os.path.join(output_dir, "document.pdf")
    text_to_pdf(text, path)
    return path, "document.pdf"
