"""
metadata/metadata_reader.py
--------------------------
Read metadata about an uploaded file.

Works in two modes:
  * filename-only  -> extension + category (no disk access needed)
  * file_path      -> additionally reads size + existence from disk

This metadata is handed to the LLM router and used by rule-based routing.

Owner: Member 3
"""

import os

from metadata.file_detector import (
    detect_category,
    get_extension,
    is_supported,
)


def read_metadata(filename: str = None, file_path: str = None) -> dict:
    """
    Build a metadata dict for a file.

    Args:
        filename:  original filename (used when the bytes aren't on disk)
        file_path: path on disk (optional; enables size detection)

    Returns:
        {
            "filename": str | None,
            "extension": str,        # "" if unknown
            "category": str,         # structured/image/document/unknown
            "supported": bool,
            "size_bytes": int | None,
            "exists": bool,
        }
    """
    # Prefer the explicit filename; otherwise derive one from the path.
    name = filename
    if not name and file_path:
        name = os.path.basename(file_path)

    exists = bool(file_path) and os.path.isfile(file_path)
    size = os.path.getsize(file_path) if exists else None

    return {
        "filename": name,
        "extension": get_extension(name) if name else "",
        "category": detect_category(name) if name else "unknown",
        "supported": is_supported(name) if name else False,
        "size_bytes": size,
        "exists": exists,
    }