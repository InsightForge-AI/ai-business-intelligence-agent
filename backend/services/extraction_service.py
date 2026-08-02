"""
==========================================================
Extraction Service
==========================================================

Responsibilities
----------------
• Validate uploaded file
• Select appropriate extractor
• Extract document content
• Return standardized extraction result
"""

from extractors.extractor_factory import get_extractor

from utils.validator import validate_file
from utils.logger import logger


def extract_document(
    file_path: str
) -> dict:
    """
    Extract document content.

    Parameters
    ----------
    file_path : str

    Returns
    -------
    dict
    """

    # -----------------------------------------------------
    # Validate File
    # -----------------------------------------------------

    validate_file(

        file_path

    )

    logger.info(

        f"Extracting document: {file_path}"

    )

    # -----------------------------------------------------
    # Select Extractor
    # -----------------------------------------------------

    extractor = get_extractor(

        file_path

    )

    # -----------------------------------------------------
    # Extract Document
    # -----------------------------------------------------

    result = extractor(

        file_path

    )

    logger.info(

        "Document extracted successfully."

    )

    # -----------------------------------------------------
    # Return Standardized Result
    # -----------------------------------------------------

    return {

        "content": result.get(

            "content",

            ""

        ),

        "pages": result.get(

            "pages",

            []

        ),

        "tables": result.get(

            "tables",

            []

        ),

        "images": result.get(

            "images",

            []

        ),

        "metadata": result.get(

            "metadata",

            {}

        )

    }