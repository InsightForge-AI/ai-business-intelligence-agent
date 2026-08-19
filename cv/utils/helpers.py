"""
==========================================================
CV Helpers
==========================================================

Common helper functions.
"""

from pathlib import Path


def get_extension(
    file_path: str
) -> str:
    """
    Return file extension.
    """

    return Path(

        file_path

    ).suffix.lower()


def is_pdf(
    file_path: str
) -> bool:
    """
    Check PDF.
    """

    return get_extension(

        file_path

    ) == ".pdf"


def is_image(
    file_path: str
) -> bool:
    """
    Check image.
    """

    return get_extension(

        file_path

    ) in [

        ".png",

        ".jpg",

        ".jpeg",

        ".bmp",

        ".tiff"

    ]


def safe_strip(
    value
):
    """
    Safely strip text.
    """

    if value is None:

        return ""

    return str(

        value

    ).strip()