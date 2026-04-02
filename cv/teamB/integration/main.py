from object_detection.detect import detect_objects
from ocr.extract_text import extract_text
from captioning.generate_caption import generate_caption

def process_image(image):
    objects = detect_objects(image)
    text = extract_text(image)
    caption = generate_caption(image)

    return {
        "objects": objects,
        "extracted_text": text,
        "description": caption
    }


# test run
if __name__ == "__main__":
    result = process_image("image.jpg")
    print(result)