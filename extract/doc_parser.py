import os
from typing import Optional

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file.
    """
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        raise ImportError("PyPDF2 is required for PDF extraction. Install with 'pip install PyPDF2'")
    text = ""
    try:
        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        raise RuntimeError(f"Failed to extract PDF text: {e}")
    return text

def extract_text_from_docx(docx_path: str) -> str:
    """
    Extracts text from a DOCX file.
    """
    try:
        import docx
    except ImportError:
        raise ImportError("python-docx is required for DOCX extraction. Install with 'pip install python-docx'")
    try:
        doc = docx.Document(docx_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        raise RuntimeError(f"Failed to extract DOCX text: {e}")

def extract_text_from_txt(txt_path: str) -> str:
    """
    Extracts text from a TXT file.
    """
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise RuntimeError(f"Failed to extract TXT text: {e}")
