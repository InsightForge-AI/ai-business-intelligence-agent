import cv2
from pathlib import Path
import json
import time

# PATHS
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed" / "captions"

MIN_AREA = 5
MAX_AREA = 500


def count_objects(image_path):
    img = cv2.imread(str(image_path))
    if img is None:
        return 0, (0, 0)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    count = sum(1 for c in contours if MIN_AREA <= cv2.contourArea(c) <= MAX_AREA)

    h, w = img.shape[:2]
    return count, (w, h)


def generate_caption(count, size):
    w, h = size

    # image size description
    if w <= 320:
        region = "small"
    elif w <= 640:
        region = "medium"
    else:
        region = "large"

    # object count description
    if count == 0:
        amount = "no visible objects"
    elif count <= 3:
        amount = "a few objects"
    elif count <= 10:
        amount = "several objects"
    else:
        amount = "many objects"

    return f"A {region} image containing {amount}."


def run():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    images = list(RAW_DIR.glob("*.jpg")) + list(RAW_DIR.glob("*.png"))

    if not images:
        print("No images found in data/raw/")
        return

    results = []

    print(f"\nProcessing {len(images)} images...\n")

    for img_path in images:
        count, size = count_objects(img_path)
        caption = generate_caption(count, size)

        print(f"{img_path.name} → {caption}")

        results.append({
            "image": img_path.name,
            "objects": count,
            "caption": caption
        })

    # save JSON
    with open(PROCESSED_DIR / "captions.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n✅ Captions saved successfully!")


if __name__ == "__main__":
    start = time.time()
    run()
    print(f"\nFinished in {time.time() - start:.2f} sec")
    print(f"\nFinished in {time.time() - start:.2f} sec")
def generate_caption(image):
    # dummy logic
    return "A person is standing near a car"
