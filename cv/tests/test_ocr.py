"""
==========================================================
OCR Tests
==========================================================

Tests OCR extraction.
"""

from analysis.image_loader import load_image
from analysis.preprocessing import preprocess_image
from analysis.ocr import run_ocr


def test_ocr():
    """
    Test OCR.
    """

    image = load_image(

        "sample_data/invoice.png"

    )

    image = preprocess_image(

        image

    )

    text, confidence = run_ocr(

        image

    )

    assert isinstance(

        text,

        str

    )

    assert len(

        text

    ) > 0

    assert isinstance(

        confidence,

        float

    )

    assert 0.0 <= confidence <= 1.0