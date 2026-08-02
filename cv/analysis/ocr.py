"""
==========================================================
OCR
==========================================================

Responsibilities
----------------
• Initialize EasyOCR
• Extract text from images
• Return extracted text
"""

import easyocr

from utils.constants import (
    OCR_LANGUAGES,
    OCR_GPU
)


# ---------------------------------------------------------
# Load EasyOCR Once
# ---------------------------------------------------------

reader = easyocr.Reader(

    OCR_LANGUAGES,

    gpu=OCR_GPU

)


def run_ocr(
    image
) -> tuple[str, float]:
    """
    Extract text from image.

    Parameters
    ----------
    image

    Returns
    -------
    tuple
        Extracted text,
        Average confidence
    """

    if image is None:

        return "", 0.0

    # -----------------------------------------------------
    # OCR
    # -----------------------------------------------------

    results = reader.readtext(

        image,

        detail=1,

        paragraph=False

    )


    if not results:

        return "", 0.0

    # -----------------------------------------------------
    # Extract Text
    # -----------------------------------------------------

    extracted_text = []

    confidence_scores = []

    for result in results:

        # Expected:
        # [bbox, text, confidence]

        if isinstance(result, (list, tuple)):

            if len(result) == 3:

                bbox, text, confidence = result

            elif len(result) == 2:

                text, confidence = result

            else:

                continue

        else:

            continue

        extracted_text.append(

            str(text)

        )

        confidence_scores.append(

            float(confidence)

        )

    if not extracted_text:

        return "", 0.0

    # -----------------------------------------------------
    # Final Text
    # -----------------------------------------------------

    text = "\n".join(

        extracted_text

    )

    average_confidence = sum(

        confidence_scores

    ) / len(

        confidence_scores

    )

    return (

        text,

        round(

            average_confidence,

            2

        )

    )