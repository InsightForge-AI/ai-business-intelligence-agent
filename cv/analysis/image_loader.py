"""
==========================================================
Image Loader
==========================================================

Responsibilities
----------------
• Load image files
• Load PDF files
• Convert PDFs to images
"""

from pathlib import Path

import cv2
import numpy as np
from pdf2image import convert_from_path


SUPPORTED_IMAGES = {
    ".png",
    ".jpg",
    ".jpeg"
}


def load_image(
    file_path: str
):
    """
    Load an image or the first page of a PDF.

    Parameters
    ----------
    file_path : str

    Returns
    -------
    numpy.ndarray
    """

    path = Path(file_path)

    if not path.exists():

        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    extension = path.suffix.lower()

    # -----------------------------------------------------
    # PDF
    # -----------------------------------------------------

    if extension == ".pdf":

        pages = convert_from_path(
            file_path,
            dpi=300
        )

        if not pages:

            raise ValueError(
                "No pages found in PDF."
            )

        return cv2.cvtColor(
            np.array(pages[0]),
            cv2.COLOR_RGB2BGR
        )

    # -----------------------------------------------------
    # Images
    # -----------------------------------------------------

    if extension in SUPPORTED_IMAGES:

        image = cv2.imread(file_path)

        if image is None:

            raise ValueError(
                f"Unable to load image: {file_path}"
            )

        return image

    # -----------------------------------------------------
    # Unsupported
    # -----------------------------------------------------

    raise ValueError(
        f"Unsupported file type for CV: {extension}. "
        "CV supports only PDF, PNG, JPG and JPEG."
    )