from PIL import Image
import easyocr

class VisionAnalyzer:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])  # English

    def analyze(self, image_path):
        result = {}

        try:
            
            image = Image.open(image_path).convert("RGB")

            ocr_result = self.reader.readtext(image_path)
            text = " ".join([res[1] for res in ocr_result])

    
            width, height = image.size

            labels = []
            if width > height:
                labels.append("landscape")
            else:
                labels.append("portrait")

            if text:
                labels.append("text")

            description = "An image with possible content"

            result["important_text"] = text if text else "No visible text"
            result["detected_objects"] = labels
            result["summary"] = f"{description}. Detected objects: {', '.join(labels)}."

            if "person" in str(labels).lower():
                result["final_insight"] = "Image likely contains a human activity." 
            elif "text" in str(labels).lower():
                result["final_insight"] = "Image contains readable content."
            else:
                result["final_insight"] = "General scene image."

            return result

        except Exception as e:
            return {"error": str(e)}