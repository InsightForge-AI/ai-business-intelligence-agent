from pathlib import Path
import json

from object_detection.detect import detect_objects
from captioning.generate_caption import generate_caption, count_objects
from ocr.extract_text import extract_text

# paths
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "processed" / "final_output"


def make_json_serializable(obj):
    """Convert numpy objects into JSON-safe format"""
    try:
        import numpy as np
        if isinstance(obj, np.ndarray):
            return obj.tolist()
    except ImportError:
        pass

    if isinstance(obj, (list, tuple)):
        return [make_json_serializable(i) for i in obj]

    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}

    return obj


def process_image(image_path):
    """Main pipeline function"""

    try:
        # detection
        detections = detect_objects(image_path)
        detections = make_json_serializable(detections[:5])  # limit

        # OCR
        text = extract_text(image_path)

        # caption
        count, size = count_objects(image_path)
        caption = generate_caption(count, size)

        return {
            "image": image_path.name,
            "objects": detections,
            "extracted_text": text,
            "description": caption
        }

    except Exception as e:
        return {"error": str(e)}


def save_results(results):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_DIR / "final_results.json", "w") as f:
        json.dump(results, f, indent=2)