"""
==========================================================
PDF Extractor
==========================================================

Responsibilities
----------------
• Read PDF document
• Extract text
• Extract page information
• Return standardized response

No AI logic.
"""

from pathlib import Path

import fitz  # PyMuPDF


def extract_pdf(
    file_path: str
) -> dict:
    """
    Extract PDF document.

    Parameters
    ----------
    file_path : str

    Returns
    -------
    dict
    """

    path = Path(file_path)

    if not path.exists():

        raise FileNotFoundError(

            f"PDF file not found: {path}"

        )

    try:

        document = fitz.open(

            path

        )

    except Exception as exc:

        raise RuntimeError(

            f"Unable to open PDF: {exc}"

        ) from exc

    # -----------------------------------------------------
    # Extract Pages
    # -----------------------------------------------------

    pages = []

    extracted_text = []

    for index, page in enumerate(document):

        text = page.get_text(

            "text"

        ).strip()

        pages.append({

            "page": index + 1,

            "text": text

        })

        extracted_text.append(

            text

        )

    # -----------------------------------------------------
    # PDF Metadata
    # -----------------------------------------------------

    pdf_metadata = document.metadata

    page_count = len(

        document

    )

    document.close()

    # -----------------------------------------------------
    # Return
    # -----------------------------------------------------

    return {

        "content": "\n".join(

            extracted_text

        ),

        "tables": [],

        "images": [],

        "pages": pages,

        "metadata": {

            "file_name": path.name,

            "document_type": "PDF",

            "page_count": page_count,

            "title": pdf_metadata.get(

                "title"

            ),

            "author": pdf_metadata.get(

                "author"

            ),

            "creator": pdf_metadata.get(

                "creator"

            ),

            "producer": pdf_metadata.get(

                "producer"

            )

        }

    }