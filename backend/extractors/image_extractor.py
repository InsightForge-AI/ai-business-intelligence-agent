"""
==========================================================
Image Extractor
==========================================================

Responsibilities
----------------
• Validate image
• Collect image metadata
• Return standardized response

No OCR.
No AI.
"""

from pathlib import Path

from PIL import Image


SUPPORTED_IMAGES = {

    ".png",

    ".jpg",

    ".jpeg"

}


def extract_image(
    file_path: str
) -> dict:
    """
    Extract image metadata.

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

            f"Image not found: {path}"

        )

    extension = path.suffix.lower()

    if extension not in SUPPORTED_IMAGES:

        raise ValueError(

            f"Unsupported image format: {extension}"

        )

    try:

        with Image.open(path) as image:

            width, height = image.size

            image_format = image.format

            image_mode = image.mode

    except Exception as exc:

        raise RuntimeError(

            f"Unable to open image: {exc}"

        ) from exc

    return {

        "content": "",

        "tables": [],

        "images": [

            str(path)

        ],

        "metadata": {

            "file_name": path.name,

            "document_type": "Image",

            "width": width,

            "height": height,

            "format": image_format,

            "mode": image_mode

        }

    }