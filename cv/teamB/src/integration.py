from src.ocr import extract_text
from src.labeling import analyze_image_bytes
from src.description import describe_image_bytes

async def process_image(file):
    try:
        # ✅ Read ONCE
        contents = await file.read()

        # OCR (file path ke liye temp save)
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as f:
            f.write(contents)

        text = extract_text(file_path)

        # ✅ SAME BYTES use karo
        labels = await analyze_image_bytes(contents)
        description = await describe_image_bytes(contents)

        return {
            "text": text,
            "labels": labels,
            "description": description
        }

    except Exception as e:
        print("INTEGRATION ERROR:", e)
        return {
            "text": "",
            "labels": [],
            "description": "",
            "error": str(e)
        }