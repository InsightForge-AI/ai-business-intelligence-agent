"""
==========================================================
CV Validators
==========================================================

Validation utilities.
"""

from utils.constants import (
    SUPPORTED_IMAGE_TYPES,
    SUPPORTED_DOCUMENT_TYPES
)


def validate_file(
    file_path: str
):
    """
    Validate supported file.
    """

    extension = file_path.lower().split(

        "."

    )[-1]

    extension = "." + extension

    supported = (

        SUPPORTED_IMAGE_TYPES +

        SUPPORTED_DOCUMENT_TYPES

    )

    if extension not in supported:

        raise ValueError(

            f"Unsupported file type: {extension}"

        )

    return True