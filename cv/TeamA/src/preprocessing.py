import os
import cv2
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "raw"))
CLEAN_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "cleaned"))
print("RAW_PATH:", RAW_PATH)
print("EXISTS:", os.path.exists(RAW_PATH))
for category in os.listdir(RAW_PATH):
    raw_folder = os.path.join(RAW_PATH, category)
    clean_folder = os.path.join(CLEAN_PATH, category)
    os.makedirs(clean_folder, exist_ok=True)
def preprocess_image(img_path):
    img = cv2.imread(img_path)
    if img is None:
        return None
    img = cv2.resize(img, (128, 128))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    normalized = blur / 255.0
    return normalized

def process_dataset():
    for category in os.listdir(RAW_PATH):
        raw_folder = os.path.join(RAW_PATH, category)
        clean_folder = os.path.join(CLEAN_PATH, category)
        for img_name in os.listdir(raw_folder):
            img_path = os.path.join(raw_folder, img_name)
            if not os.path.isfile(img_path):
                continue
            if not img_name.lower().endswith(('.jpg', '.png', '.jpeg')):
                continue
            processed_img = preprocess_image(img_path)

            if processed_img is not None:
                save_path = os.path.join(clean_folder, img_name)
                processed_img = (processed_img * 255).astype("uint8")
                cv2.imwrite(save_path, processed_img)

if __name__ == "__main__":
    process_dataset()
    print("✅ Preprocessing Done!")