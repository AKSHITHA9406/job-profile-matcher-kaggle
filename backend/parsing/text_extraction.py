from pathlib import Path
import fitz  # PyMuPDF
from docx import Document

class TextExtractionError(Exception):
    pass

def extract_text_from_pdf(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise TextExtractionError(f"PDF file not found: {p.resolve()}")
    try:
        doc = fitz.open(path)
    except Exception as e:
        raise TextExtractionError(f"Failed to open PDF '{p}': {e}")
    texts = [page.get_text("text") for page in doc]
    if not texts:
        raise TextExtractionError(f"No text extracted from PDF: {p.resolve()}")
    return "\n".join(texts)

def extract_text_from_docx(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise TextExtractionError(f"DOCX file not found: {p.resolve()}")
    try:
        document = Document(path)
    except Exception as e:
        raise TextExtractionError(f"Failed to open DOCX '{p}': {e}")
    texts = [para.text for para in document.paragraphs]
    if not texts:
        raise TextExtractionError(f"No text extracted from DOCX: {p.resolve()}")
    return "\n".join(texts)

def extract_text_any(path: str) -> str:
    suffix = Path(path).suffix.lower()
    if suffix == ".pdf":
        return extract_text_from_pdf(path)
    if suffix in (".doc", ".docx"):
        return extract_text_from_docx(path)
    raise TextExtractionError(f"Unsupported file type: '{suffix}' for file {path}")
