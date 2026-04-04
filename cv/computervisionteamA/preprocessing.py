import cv2
import os
INPUT_IMAGE_PATH = "image.jpg"   # put your image in same folder
OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
image = cv2.imread(INPUT_IMAGE_PATH)
if image is None:
    print("Error: Image not found!")
    exit()
print("Image loaded successfully")
resized = cv2.resize(image, (500, 500))
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blur, 100, 200)
equalized = cv2.equalizeHist(gray)
cv2.imwrite(os.path.join(OUTPUT_FOLDER, "resized.jpg"), resized)
cv2.imwrite(os.path.join(OUTPUT_FOLDER, "gray.jpg"), gray)
cv2.imwrite(os.path.join(OUTPUT_FOLDER, "blur.jpg"), blur)
cv2.imwrite(os.path.join(OUTPUT_FOLDER, "edges.jpg"), edges)
cv2.imwrite(os.path.join(OUTPUT_FOLDER, "equalized.jpg"), equalized)
print("Processed images saved in 'output' folder")
cv2.imshow("Original", image)
cv2.imshow("Resized", resized)
cv2.imshow("Gray", gray)
cv2.imshow("Blur", blur)
cv2.imshow("Edges", edges)
cv2.imshow("Equalized", equalized)
cv2.waitKey(0)
cv2.destroyAllWindows()