import os
import cv2
from ultralytics import YOLO
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "cleaned"))
OUTPUT_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "detected"))
os.makedirs(OUTPUT_PATH, exist_ok=True)
print("INPUT_PATH:", INPUT_PATH)
print("OUTPUT_PATH:", OUTPUT_PATH)
model = YOLO("yolov8n.pt")  # lightweight model
TARGET_CLASSES = ["car", "motorcycle"]
def detect_objects(image_path):
    results = model(image_path)
    image = cv2.imread(image_path)
    if image is None:
        print("Skipping:", image_path)
        return None
    for r in results:
        boxes = r.boxes
        names = r.names
        for box in boxes:
            cls_id = int(box.cls[0])
            label = names[cls_id]
            if label not in TARGET_CLASSES:
                continue
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            text = f"{label}: {conf:.2f}"
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, text, (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
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
            detected_img = detect_objects(img_path)
            if detected_img is not None:
                save_path = os.path.join(output_folder, img_name)
                cv2.imwrite(save_path, detected_img)
if __name__ == "__main__":
    process_dataset()
    print("✅ YOLO Detection Done!")