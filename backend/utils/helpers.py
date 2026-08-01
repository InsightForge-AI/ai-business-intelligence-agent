"""
==========================================================
Helpers
==========================================================

Common helper functions used across the Backend.
"""

from pathlib import Path
from uuid import uuid4


def generate_file_id() -> str:
    """
    Generate a unique file ID.
    """

    return str(

        uuid4()

    )


def get_file_extension(
    file_name: str
) -> str:
    """
    Return lowercase file extension.
    """

    return Path(

        file_name

    ).suffix.lower()


def get_file_name(
    file_path: str
) -> str:
    """
    Return filename from path.
    """

    return Path(

        file_path

    ).name


def get_stored_filename(
    file_id: str,
    extension: str
) -> str:
    """
    Generate stored filename.
    """

    return f"{file_id}{extension}"


def calculate_word_count(
    text: str
) -> int:
    """
    Calculate word count.
    """

    if not text:

        return 0

    return len(

        text.split()

    )


def safe_get(
    data: dict,
    key: str,
    default=None
):
    """
    Safely retrieve a dictionary value.
    """

    return data.get(

        key,

        default

    )