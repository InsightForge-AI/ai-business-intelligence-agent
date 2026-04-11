import easyocr

# 🔥 initialize once (important for performance)
reader = easyocr.Reader(['en'], gpu=False)


def extract_text(image_path):
    """
    Extract text from image using EasyOCR
    Returns: list of detected text
    """

    try:
        results = reader.readtext(str(image_path))

        # filter text based on confidence
        texts = []
        for (_, text, conf) in results:
            if conf > 0.3:
                texts.append(text)

        # 🔥 limit output (important for API size)
        return texts[:5]

    except Exception as e:
        return [f"OCR error: {str(e)}"]