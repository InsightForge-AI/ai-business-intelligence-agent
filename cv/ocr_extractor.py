# ocr_extractor.py
# Narayani | Sprint 5 Task: EasyOCR integration + Text extraction + OCR accuracy testing
# INPUT  : Image file (invoice or receipt)
# OUTPUT : Extracted text string → passed to Nadita's document_classifier.py

import easyocr
from PIL import Image
import numpy as np
import cv2
import os
import json


# ─────────────────────────────────────────────
# STEP 1: LOAD IMAGE FROM FILE PATH
# ─────────────────────────────────────────────
def load_image(image_path: str) -> np.ndarray:
    """
    INPUT  : path to image file (jpg / png)
    OUTPUT : numpy array (BGR image)
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at path: {image_path}")

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"Could not read image: {image_path}")

    print(f"[✔] Image loaded successfully: {image_path}")
    return image


# ─────────────────────────────────────────────
# STEP 2: PREPROCESS IMAGE
# (Shruti handles full preprocessing —
#  this is a basic fallback for standalone run)
# ─────────────────────────────────────────────
def preprocess(image: np.ndarray) -> np.ndarray:
    """
    INPUT  : BGR numpy image array
    OUTPUT : grayscale + thresholded numpy image array
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    print("[✔] Image preprocessed (grayscale + threshold)")
    return thresh


# ─────────────────────────────────────────────
# STEP 3: TEXT EXTRACTION USING EASYOCR
# ─────────────────────────────────────────────
def extract_text_easyocr(image: np.ndarray) -> str:
    """
    INPUT  : preprocessed numpy image array
    OUTPUT : extracted text as a single string
    """
    print("[...] Running EasyOCR extraction...")
    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(image, detail=0)
    text = "\n".join(results)
    print("[✔] EasyOCR extraction complete")
    return text


# ─────────────────────────────────────────────
# STEP 4: OCR ACCURACY TESTING
# (for invoices and receipts)
# ─────────────────────────────────────────────
def test_ocr_accuracy(image: np.ndarray, ground_truth: str) -> dict:
    """
    INPUT  : preprocessed image, ground truth text
    OUTPUT : accuracy report dict — printed to terminal
    """
    extracted = extract_text_easyocr(image)

    gt_words = set(ground_truth.lower().split())
    ext_words = set(extracted.lower().split())
    matched = gt_words & ext_words
    missed = gt_words - ext_words
    accuracy = round(len(matched) / len(gt_words) * 100, 2) if gt_words else 0.0

    report = {
        "method": "easyocr",
        "accuracy_percent": accuracy,
        "extracted_text": extracted,
        "matched_words": sorted(matched),
        "missed_words": sorted(missed)
    }

    print("\n[✔] Accuracy Report:")
    print(json.dumps(report, indent=2))
    return report


# ─────────────────────────────────────────────
# STEP 5: MAIN PIPELINE FUNCTION
# Called by Team Lead's /cv/analyze API
# ─────────────────────────────────────────────
def run_ocr(image_bytes: bytes) -> str:
    """
    INPUT  : raw image bytes from Flask API upload request
    OUTPUT : extracted text string → passed to Nadita's analyze_document()
    """
    np_arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    processed = preprocess(image)
    return extract_text_easyocr(processed)


# ─────────────────────────────────────────────
# STANDALONE TEST
# Run: python ocr_extractor.py
# INPUT  : sample_invoice.png in same folder
# OUTPUT : extracted text printed in terminal
# ─────────────────────────────────────────────
if __name__ == "__main__":

    # ✅ Change this to your actual test image path
    IMAGE_PATH = "sample_invoice.png"

    print("=" * 55)
    print("  NARAYANI — OCR EXTRACTOR | SPRINT 5")
    print("=" * 55)

    # Load image
    image = load_image(IMAGE_PATH)

    # Preprocess
    processed = preprocess(image)

    # EasyOCR extraction
    print("\n─── EasyOCR Result ───────────────────────────────")
    easyocr_text = extract_text_easyocr(processed)
    print("\nINPUT  :", IMAGE_PATH)
    print("OUTPUT (EasyOCR):\n")
    print(easyocr_text)

    # Accuracy test
    print("\n─── Accuracy Test ────────────────────────────────")
    # ✅ Replace with actual expected text from your test image
    GROUND_TRUTH = "Invoice 123456 Date 5/1/2014 Total 551.56 Service Fee Labor Tax"
    report = test_ocr_accuracy(processed, GROUND_TRUTH)
    print(f"\n[✔] Final Accuracy: {report['accuracy_percent']}%")

    print("\n" + "=" * 55)
    print("  TEXT READY → passing to Nadita's module")
    print("=" * 55)
    print(easyocr_text)