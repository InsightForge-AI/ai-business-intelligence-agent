"""
==========================================================
Extractor Factory
==========================================================

Responsibilities
----------------
• Detect document type
• Select appropriate extractor
• Return extractor function
"""

from pathlib import Path

from extractors.csv_extractor import extract_csv
from extractors.docx_extractor import extract_docx
from extractors.excel_extractor import extract_excel
from extractors.image_extractor import extract_image
from extractors.pdf_extractor import extract_pdf


EXTRACTOR_MAP = {

    ".csv": extract_csv,

    ".xlsx": extract_excel,

    ".xls": extract_excel,

    ".pdf": extract_pdf,

    ".png": extract_image,

    ".jpg": extract_image,

    ".jpeg": extract_image,

    ".docx": extract_docx

}


def get_extractor(
    file_path: str
):
    """
    Return extractor for a document.

    Parameters
    ----------
    file_path : str

    Returns
    -------
    callable
    """

    extension = Path(

        file_path

    ).suffix.lower()

    extractor = EXTRACTOR_MAP.get(

        extension

    )

    if extractor is None:

        raise ValueError(

            f"No extractor registered for '{extension}'."

        )

    return extractor