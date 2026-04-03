import cv2
import numpy as np
from pathlib import Path
import json
import time

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
BASE_DIR      = Path(__file__).resolve().parent.parent  # cv/teamB/
RAW_DIR       = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed" / "captions"

CLASSES  = ["fish", "fly", "honeybee", "seagull"]
MIN_AREA = 5
MAX_AREA = 500


# ─────────────────────────────────────────────
# COUNT OBJECTS IN IMAGE
# ─────────────────────────────────────────────
def count_objects(image_path):
    img = cv2.imread(str(image_path))
    if img is None:
        return 0, (0, 0)

    gray    = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh  = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        blockSize=11, C=2
    )
    kernel  = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    opened  = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    contours, _ = cv2.findContours(opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    count = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if MIN_AREA <= area <= MAX_AREA:
            count += 1

    h, w = img.shape[:2]
    return count, (w, h)


# ─────────────────────────────────────────────
# GENERATE CAPTION
# ─────────────────────────────────────────────
def generate_caption(cls, count, image_size):
    w, h   = image_size
    region = "small" if w <= 320 else "medium" if w <= 640 else "large"

    if count == 0:
        amount = "no visible"
    elif count <= 3:
        amount = "a few"
    elif count <= 10:
        amount = "several"
    elif count <= 30:
        amount = "many"
    else:
        amount = "a large number of"

    # class specific captions
    captions = {
        "fish":     f"A {region} underwater image containing {amount} small fish.",
        "fly":      f"A {region} image showing {amount} flies in the scene.",
        "honeybee": f"A {region} image with {amount} honeybees visible.",
        "seagull":  f"A {region} aerial image containing {amount} seagulls."
    }

    return captions.get(cls, f"An image containing {amount} {cls} objects.")


# ─────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────
def run():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    all_captions = []

    for cls in CLASSES:
        img_dir = RAW_DIR / cls / "img"
        out_dir = PROCESSED_DIR / cls
        out_dir.mkdir(parents=True, exist_ok=True)

        if not img_dir.exists():
            print(f"[SKIP] {cls} - folder not found")
            continue

        images = sorted(img_dir.glob("*.jpg")) + sorted(img_dir.glob("*.png"))
        if not images:
            print(f"[SKIP] {cls} - no images found")
            continue

        print(f"\n{'='*55}")
        print(f"  Class: {cls}  ({len(images)} images)")
        print(f"{'='*55}")

        class_captions = []

        for img_path in images:
            # count objects
            count, size = count_objects(img_path)

            # generate caption
            caption = generate_caption(cls, count, size)

            print(f"  {img_path.name:30s} | objects={count:3d} | {caption}")

            class_captions.append({
                "image":   img_path.name,
                "class":   cls,
                "objects": count,
                "caption": caption
            })
            all_captions.append({
                "image":   img_path.name,
                "class":   cls,
                "objects": count,
                "caption": caption
            })

        # save per class captions
        with open(out_dir / "captions.json", "w") as f:
            json.dump(class_captions, f, indent=2)

        # save per class captions as text file
        with open(out_dir / "captions.txt", "w") as f:
            for item in class_captions:
                f.write(f"{item['image']}: {item['caption']}\n")

        print(f"\n  Saved -> {out_dir / 'captions.json'}")
        print(f"  Saved -> {out_dir / 'captions.txt'}")

    # save all captions together
    with open(PROCESSED_DIR / "all_captions.json", "w") as f:
        json.dump(all_captions, f, indent=2)

    with open(PROCESSED_DIR / "all_captions.txt", "w") as f:
        for item in all_captions:
            f.write(f"{item['image']}: {item['caption']}\n")

    print(f"\n{'='*55}")
    print(f"  DONE — Total images captioned: {len(all_captions)}")
    print(f"  All captions -> {PROCESSED_DIR / 'all_captions.json'}")
    print(f"  All captions -> {PROCESSED_DIR / 'all_captions.txt'}")
    print(f"{'='*55}")


# ─────────────────────────────────────────────
if __name__ == "__main__":
    t0 = time.time()
    run()
    print(f"\n  Done in {time.time() - t0:.1f}s")