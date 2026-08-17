from PIL import Image


def analyze_image(image_path):
    """Inspect a validated image file on disk and return real metadata.

    Object detection / OCR are not implemented -- this repo has no model
    for either, so those fields are reported honestly as unavailable
    instead of returning fabricated placeholder values.
    """
    with Image.open(image_path) as img:
        width, height = img.size
        return {
            "objects": [],
            "objects_note": "object detection not implemented",
            "extracted_text": None,
            "extracted_text_note": "OCR not implemented",
            "description": f"{img.format} image, {width}x{height}, mode {img.mode}",
            "width": width,
            "height": height,
            "format": img.format,
        }
