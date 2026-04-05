import sys
import json
from pathlib import Path

# Fix import path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Imports
from object_detection.detect import detect_objects
from captioning.generate_caption import generate_caption, count_objects
from ocr.extract_text import extract_text

RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "data" / "processed" / "final_output"


def make_json_serializable(obj):
    """Convert numpy and complex objects into JSON-safe format"""
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
    """Process a single image through all modules"""

    detections = make_json_serializable(detect_objects(image_path))
    text = extract_text(image_path)

    count, size = count_objects(image_path)
    caption = generate_caption(count, size)

    return {
        "image": image_path.name,
        "objects": detections,
        "extracted_text": text,
        "description": caption
    }


def run():
    """Run full pipeline"""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    images = list(RAW_DIR.glob("*.png")) + list(RAW_DIR.glob("*.jpg"))

    if not images:
        print("No images found in data/raw/")
        return

    final_results = []

    print(f"\nProcessing {len(images)} images...\n")

    for img_path in images:
        try:
            result = process_image(img_path)
            final_results.append(result)
            print(f"{img_path.name} → processed")
        except Exception as e:
            print(f"Error processing {img_path.name}: {e}")

    output_file = OUTPUT_DIR / "final_results.json"

    with open(output_file, "w") as f:
        json.dump(final_results, f, indent=2)

    print(f"\n✅ Final output saved at: {output_file}")


if __name__ == "__main__":
    run()