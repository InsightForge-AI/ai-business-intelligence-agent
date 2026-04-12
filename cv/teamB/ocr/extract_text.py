import easyocr
from pathlib import Path
import json

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "data" / "processed" / "ocr"

# OCR model
reader = easyocr.Reader(['en'], gpu=False)

def extract_text(image_path):
    results = reader.readtext(str(image_path))
    return [text for (_, text, conf) in results if conf > 0.3]

def run():
    print("📂 Using path:", RAW_DIR)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    images = list(RAW_DIR.glob("*.png")) + list(RAW_DIR.glob("*.jpg"))

    if not images:
        print("❌ No images found")
        return

    all_results = []

    for img in images:
        text = extract_text(img)
        print(img.name, "→", text)

        all_results.append({
            "image": img.name,
            "text": text
        })

    with open(OUTPUT_DIR / "ocr_results.json", "w") as f:
        json.dump(all_results, f, indent=2)

    print("✅ Done!")

if __name__ == "__main__":
    run()
    run()
def extract_text(image):
    # dummy logic
    return "Sample extracted text"
