import re
from typing import Any

def clean_text(text: str) -> str:
    """
    Cleans input text by removing extra whitespace, non-printable characters, and normalizing spaces.
    """
    if not isinstance(text, str):
        raise ValueError("Input to clean_text must be a string.")
    text = text.replace('\xa0', ' ')
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x20-\x7E]", "", text)
    return text.strip()
