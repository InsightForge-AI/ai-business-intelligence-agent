import cv2
from pathlib import Path
import json
import time

# PATHS
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

MIN_AREA = 5
MAX_AREA = 500


def detect_objects(image_path):
    img = cv2.imread(str(image_path))
    if img is None:
        raise FileNotFoundError(f"Cannot read: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    thresh = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detections = []
    annotated = img.copy()

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if MIN_AREA <= area <= MAX_AREA:
            x, y, w, h = cv2.boundingRect(cnt)

            detections.append({
                "x": int(x),
                "y": int(y),
                "w": int(w),
                "h": int(h)
            })

            cv2.rectangle(annotated, (x, y), (x+w, y+h), (0, 255, 0), 1)

    return detections, annotated


def run():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    images = list(RAW_DIR.glob("*.png")) + list(RAW_DIR.glob("*.jpg"))

    if not images:
        print("No images found in data/raw/")
        return

    results = []

    print(f"\nProcessing {len(images)} images...\n")

    for img_path in images:
        try:
            detections, annotated = detect_objects(img_path)
        except Exception as e:
            print(f"Error: {img_path.name} → {e}")
            continue

        # save image
        out_path = PROCESSED_DIR / f"det_{img_path.name}"
        cv2.imwrite(str(out_path), annotated)

        results.append({
            "image": img_path.name,
            "objects": ["box"],  # dummy output (as per task)
            "detections": detections,
            "description": "basic image"
        })

        print(f"{img_path.name} → {len(detections)} objects")

    # save JSON
    with open(PROCESSED_DIR / "summary.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n✅ Done! Output saved in processed folder")


if __name__ == "__main__":
    start = time.time()
    run()
    print(f"\nFinished in {time.time() - start:.2f} sec")