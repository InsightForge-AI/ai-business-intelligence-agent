import easyocr
import numpy as np
import cv2
import os
import json

# Load EasyOCR model only once
print("[INFO] Loading EasyOCR model...")
reader = easyocr.Reader(['en'], gpu=False)
print("[INFO] EasyOCR model loaded successfully.")


# ==========================================
# IMAGE LOADING
# ==========================================
def load_image(image_path: str) -> np.ndarray:
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(
                f"Image not found at path: {image_path}"
            )

        image = cv2.imread(image_path)

        if image is None:
            raise ValueError(
                f"Could not read image: {image_path}"
            )

        return image

    except Exception as e:
        print(f"[ERROR] Failed to load image: {str(e)}")
        raise


# ==========================================
# IMAGE PREPROCESSING
# ==========================================
def preprocess(image: np.ndarray) -> np.ndarray:
    try:
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Resize image (helps OCR read small text)
        gray = cv2.resize(
            gray,
            None,
            fx=4,      
            fy=4,     
            interpolation=cv2.INTER_CUBIC
        )

        # Noise removal
        gray = cv2.GaussianBlur(gray, (3, 3), 0)

        # Contrast enhancement
        gray = cv2.equalizeHist(gray)

        # Adaptive Thresholding (better than OTSU for invoices)
        thresh = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )

        # Morphological operation
        kernel = np.ones((2, 2), np.uint8)
        thresh = cv2.morphologyEx(
            thresh,
            cv2.MORPH_CLOSE,
            kernel
        )

        return thresh

    except Exception as e:
        print(f"[ERROR] Image preprocessing failed: {str(e)}")
        raise


# ==========================================
# OCR EXTRACTION
# ==========================================
def extract_text_easyocr(image: np.ndarray) -> tuple:

    try:
        print("[INFO] Running EasyOCR...")

        results = reader.readtext(
            image,
            detail=1,
            paragraph=False,
            width_ths=0.7,    
            height_ths=0.7    
        )

        if not results:
            return "", 0.0

        extracted_lines = []
        confidences = []

        for result in results:
            extracted_lines.append(result[1])
            confidences.append(result[2])

        extracted_text = "\n".join(extracted_lines)

        avg_confidence = round(
            (sum(confidences) / len(confidences)) * 100,
            2
        )

        return (
            extracted_text,
            avg_confidence
        )

    except Exception as e:
        print(
            f"[ERROR] OCR Extraction Failed: {str(e)}"
        )
        return "", 0.0


# ==========================================
# OCR ACCURACY TEST
# ==========================================
def test_ocr_accuracy(
    image: np.ndarray,
    ground_truth: str
) -> dict:

    extracted, confidence = (
        extract_text_easyocr(image)
    )

    gt_words = set(
        ground_truth.lower().split()
    )

    ext_words = set(
        extracted.lower().split()
    )

    matched = gt_words & ext_words
    missed = gt_words - ext_words

    accuracy = (
        round(
            len(matched)
            / len(gt_words)
            * 100,
            2
        )
        if gt_words
        else 0.0
    )

    return {
        "method": "easyocr",
        "accuracy_percent": accuracy,
        "ocr_confidence_percent": confidence,
        "extracted_text": extracted,
        "matched_words": sorted(matched),
        "missed_words": sorted(missed)
    }


# ==========================================
# MAIN FUNCTION
# ==========================================
def run_ocr(
    image_bytes: bytes
) -> str:

    try:

        if not image_bytes:
            raise ValueError(
                "Empty image bytes received."
            )

        np_arr = np.frombuffer(
            image_bytes,
            np.uint8
        )

        image = cv2.imdecode(
            np_arr,
            cv2.IMREAD_COLOR
        )

        if image is None:
            raise ValueError(
                "Invalid image format or corrupted image."
            )

        processed = preprocess(image)

        extracted_text, confidence = (
            extract_text_easyocr(
                processed
            )
        )

        print(
            f"[INFO] OCR Confidence: "
            f"{confidence}%"
        )

        # Change 3: OCR text debug print
        print("\n===== OCR TEXT =====")
        print(extracted_text)
        print("====================")

        return extracted_text

    except Exception as e:
        print(
            f"[ERROR] OCR Pipeline Failed: {str(e)}"
        )
        return ""


# ==========================================
# STANDALONE TEST
# ==========================================
if __name__ == "__main__":

    IMAGE_PATH = "sample_invoice.png"

    try:

        image = load_image(
            IMAGE_PATH
        )

        processed = preprocess(
            image
        )

        text, confidence = (
            extract_text_easyocr(
                processed
            )
        )

        print(
            "\n===== OCR OUTPUT =====\n"
        )

        print(text)

        print(
            f"\nOCR Confidence: "
            f"{confidence}%"
        )

    except Exception as e:
        print(
            f"[FATAL ERROR] {str(e)}"
        )