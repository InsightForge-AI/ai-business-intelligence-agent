import sys
from pathlib import Path
import json

# fix import path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# imports
from object_detection.detect import detect_objects
from captioning.generate_caption import generate_caption, count_objects
from ocr.extract_text import extract_text

RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "data" / "processed" / "final_output"


# 🔥 recursive converter (handles all numpy types)
def make_json_serializable(obj):
    try:
        import numpy as np
    except ImportError:
        np = None

    if np and isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, list):
        return [make_json_serializable(i) for i in obj]
    elif isinstance(obj, tuple):
        return [make_json_serializable(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    else:
        return obj


def process_image(image_path):
    # object detection
    detections = detect_objects(image_path)

    # 🔥 FIX: convert everything to JSON-safe
    detections = make_json_serializable(detections)

    # OCR
    text = extract_text(image_path)

    # captioning
    count, size = count_objects(image_path)
    caption = generate_caption(count, size)

    return {
        "image": image_path.name,
        "objects": detections,
        "extracted_text": text,
        "description": caption
    }


def run():
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
            print(f"Error: {img_path.name} → {e}")

    # 🔥 FINAL SAFE DUMP
    with open(OUTPUT_DIR / "final_results.json", "w") as f:
        json.dump(make_json_serializable(final_results), f, indent=2)

    print("\n✅ Final output generated!")


if __name__ == "__main__":
    run()