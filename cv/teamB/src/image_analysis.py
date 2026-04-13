from src.detect import detect_objects
from src.ocr import extract_text
from src.describe import describe_image

def analyze_image(image_path):
    return {
        "objects": detect_objects(image_path),
        "extracted_text": extract_text(image_path),
        "description": describe_image(image_path)
def analyze_image(image):
    return {
        "objects": ["box"],
        "extracted_text": "sample",
        "description": "basic image"
    }