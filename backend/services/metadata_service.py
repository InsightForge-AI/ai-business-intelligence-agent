"""
==========================================================
Metadata Service
==========================================================

Generate standardized metadata for all supported
document types.

Responsibilities
----------------
• Generate common metadata
• Merge extractor metadata
• Normalize document information

Supports:
• Text documents
• Structured datasets (CSV/Excel)
"""

from datetime import datetime


def generate_metadata(
    file_info: dict,
    extracted_data: dict
) -> dict:
    """
    Generate metadata for an extracted document.

    Parameters
    ----------
    file_info : dict

    extracted_data : dict

    Returns
    -------
    dict
    """

    extractor_metadata = extracted_data.get(
        "metadata",
        {}
    )

    content = extracted_data.get(
        "content",
        ""
    )

    # -----------------------------------------------------
    # Calculate Word Count
    # -----------------------------------------------------

    if isinstance(content, str):

        word_count = len(content.split())

    elif isinstance(content, list):

        # Structured datasets (Excel / CSV)
        rows = len(content)

        columns = (
            len(content[0])
            if rows > 0 and isinstance(content[0], dict)
            else 0
        )

        # Approximate total values stored
        word_count = rows * columns

    elif isinstance(content, dict):

        word_count = len(content)

    else:

        word_count = 0

    # -----------------------------------------------------
    # Metadata
    # -----------------------------------------------------

    metadata = {

        "file_id": file_info.get(
            "file_id"
        ),

        "file_name": file_info.get(
            "file_name"
        ),

        "file_type": file_info.get(
            "file_type"
        ),

        "file_size": file_info.get(
            "file_size"
        ),

        "generated_at": datetime.utcnow().isoformat(),

        "document_type": extractor_metadata.get(
            "document_type",
            "Unknown"
        ),

        "word_count": word_count,

        "page_count": len(
            extracted_data.get(
                "pages",
                []
            )
        ),

        "table_count": len(
            extracted_data.get(
                "tables",
                []
            )
        ),

        "image_count": len(
            extracted_data.get(
                "images",
                []
            )
        )

    }

    # -----------------------------------------------------
    # Merge Extractor Metadata
    # -----------------------------------------------------

    metadata.update(
        extractor_metadata
    )

    return metadata