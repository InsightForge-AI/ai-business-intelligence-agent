"""
metadata/file_detection.py
-------------------------
Detect a file's type/category from its name (and optionally its bytes).

Owner: Member 3
"""

import os

from utils.constants import (
    DOCUMENT_EXTS,
    IMAGE_EXTS,
    STRUCTURED_EXTS,
    SUPPORTED_EXTS,
)

# Map each category to a human label.
CATEGORY_DOCUMENT = "document"
CATEGORY_STRUCTURED = "structured"
CATEGORY_IMAGE = "image"
CATEGORY_UNKNOWN = "unknown"


def get_extension(filename: str) -> str:
    """Return the lower-cased extension including the dot, or ''."""
    if not filename:
        return ""
    return os.path.splitext(filename)[1].lower()


def detect_category(filename: str) -> str:
    """Classify a file into structured / image / document / unknown."""
    ext = get_extension(filename)
    if ext in STRUCTURED_EXTS:
        return CATEGORY_STRUCTURED
    if ext in IMAGE_EXTS:
        return CATEGORY_IMAGE
    if ext in DOCUMENT_EXTS:
        return CATEGORY_DOCUMENT
    return CATEGORY_UNKNOWN


def is_supported(filename: str) -> bool:
    """True if we recognise and accept this file type."""
    return get_extension(filename) in SUPPORTED_EXTS