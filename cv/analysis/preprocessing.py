"""
==========================================================
Image Preprocessing
==========================================================

Responsibilities
----------------
• Resize image
• Convert to grayscale
• Reduce noise
• Improve contrast
• Apply thresholding
"""

import cv2


def preprocess_image(
    image
):
    """
    Preprocess image for OCR.

    Parameters
    ----------
    image

    Returns
    -------
    image
    """

    if image is None:

        raise ValueError(

            "Invalid image."

        )

    # -----------------------------------------------------
    # Resize
    # -----------------------------------------------------

    image = cv2.resize(

        image,

        None,

        fx=2,

        fy=2,

        interpolation=cv2.INTER_CUBIC

    )

    # -----------------------------------------------------
    # Grayscale
    # -----------------------------------------------------

    gray = cv2.cvtColor(

        image,

        cv2.COLOR_BGR2GRAY

    )

    # -----------------------------------------------------
    # Noise Removal
    # -----------------------------------------------------

    gray = cv2.GaussianBlur(

        gray,

        (5, 5),

        0

    )

    # -----------------------------------------------------
    # Contrast Enhancement
    # -----------------------------------------------------

    gray = cv2.equalizeHist(

        gray

    )

    # -----------------------------------------------------
    # Adaptive Threshold
    # -----------------------------------------------------

    processed = cv2.adaptiveThreshold(

        gray,

        255,

        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

        cv2.THRESH_BINARY,

        11,

        2

    )

    # -----------------------------------------------------
    # Morphological Cleanup
    # -----------------------------------------------------

    kernel = cv2.getStructuringElement(

        cv2.MORPH_RECT,

        (2, 2)

    )

    processed = cv2.morphologyEx(

        processed,

        cv2.MORPH_CLOSE,

        kernel

    )

    return processed