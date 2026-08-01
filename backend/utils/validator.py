"""
==========================================================
Validator
==========================================================

Responsibilities
----------------
• Validate uploaded files
• Validate stored files

No FastAPI-specific logic.
"""

from pathlib import Path

from utils.constants import SUPPORTED_EXTENSIONS


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