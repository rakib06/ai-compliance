from typing import List
import io
try:
    import pytesseract
    from PIL import Image
    from pdf2image import convert_from_bytes
except Exception:
    pytesseract = None

def ocr_bytes(data: bytes, filename: str) -> str:
    """Simple OCR for images or PDFs using Tesseract. For PDFs, rasterize pages."""
    if filename.lower().endswith(".pdf"):
        if 'convert_from_bytes' not in globals():
            return ""
        pages = convert_from_bytes(data, dpi=200)
        text_pages: List[str] = []
        for img in pages:
            text_pages.append(pytesseract.image_to_string(img) if pytesseract else "")
        return "\n".join(text_pages)
    else:
        if 'Image' not in globals():
            return ""
        img = Image.open(io.BytesIO(data))
        return pytesseract.image_to_string(img) if pytesseract else ""
