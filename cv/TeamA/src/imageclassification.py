import os
import cv2
from ultralytics import YOLO
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "cleaned"))
OUTPUT_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "classified"))
os.makedirs(OUTPUT_PATH, exist_ok=True)
print("INPUT_PATH:", INPUT_PATH)
print("OUTPUT_PATH:", OUTPUT_PATH)
model = YOLO("yolov8n-cls.pt")  # auto downloads
def classify_image(image_path):
    results = model(image_path)
    image = cv2.imread(image_path)
    if image is None:
        print("Skipping:", image_path)
        return None
    for r in results:
        probs = r.probs
        top1 = probs.top1  # class index
        confidence = probs.top1conf.item()
        label = r.names[top1]
        text = f"{label}: {confidence:.2f}"
        cv2.putText(image, text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2)
    return image
def process_dataset():
    valid_ext = ('.jpg', '.jpeg', '.png')
    for category in os.listdir(INPUT_PATH):
        input_folder = os.path.join(INPUT_PATH, category)
        output_folder = os.path.join(OUTPUT_PATH, category)
        if not os.path.isdir(input_folder):
            continue
        os.makedirs(output_folder, exist_ok=True)
        for img_name in os.listdir(input_folder):
            if not img_name.lower().endswith(valid_ext):
                continue
            img_path = os.path.join(input_folder, img_name)
            classified_img = classify_image(img_path)
            if classified_img is not None:
                save_path = os.path.join(output_folder, img_name)
                cv2.imwrite(save_path, classified_img)
if __name__ == "__main__":
    process_dataset()
    print("✅ Image Classification Done!")