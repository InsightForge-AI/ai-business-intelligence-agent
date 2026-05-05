import pytesseract
import cv2

def extract_text(image_path):
    try:
        # Image read karo
        img = cv2.imread(image_path)

        # Check if image loaded
        if img is None:
            return ""

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Noise removal
        gray = cv2.medianBlur(gray, 3)

        # Threshold (better OCR)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # OCR
        text = pytesseract.image_to_string(thresh)

        return text.strip()

    except Exception as e:
        print("OCR Error:", e)
        return ""