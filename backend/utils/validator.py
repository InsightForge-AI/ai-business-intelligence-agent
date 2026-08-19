"""
==========================================================
Validator
==========================================================

Responsibilities
----------------
• Validate uploaded files
• Validate stored files
• Validate document identifiers

No FastAPI-specific logic.
"""

from pathlib import Path
from uuid import UUID

from utils.constants import SUPPORTED_EXTENSIONS


def validate_document_id(document_id: str) -> str:
    """
    Validate a document ID before it is used to build any filesystem path.

    Every stored document's ID is a uuid4() (see
    services/storage_service.py), so this both rejects path-traversal
    payloads (e.g. "../../etc/passwd") and non-existent IDs early, rather
    than trusting a raw URL path segment to build
    `f"{document_id}.json"` directly, which is not safe on its own.

    Returns the validated ID (normalized to the canonical uuid4 string
    form) so callers can use the return value directly.
    """

    try:
        return str(UUID(str(document_id)))
    except (ValueError, AttributeError, TypeError):
        raise ValueError(f"Invalid document id: {document_id!r}")


def validate_upload(file) -> None:
    """
    Validate uploaded file.
    """

    extension = Path(

        file.filename

    ).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:

        raise ValueError(

            f"Unsupported file format: {extension}"

        )


def validate_file(
    file_path: str
) -> None:
    """
    Validate stored file.
    """

    path = Path(

        file_path

    )

    if not path.exists():

        raise FileNotFoundError(

            f"File not found: {path}"

        )

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:

        raise ValueError(

            f"Unsupported file format: {extension}"

        )