from teamB.src.ocr import extract_text
from teamB.src.labeling import analyze_image_bytes
from teamB.src.description import describe_image_bytes


async def process_image(file):

    try:
        # ✅ Read image ONCE
        contents = await file.read()

        # ✅ Save temp image for OCR
        file_path = f"temp_{file.filename}"

        with open(file_path, "wb") as f:
            f.write(contents)

        # ✅ OCR
        text = extract_text(file_path)

        # ✅ Labeling
        labels = await analyze_image_bytes(contents)

        # ✅ Description
        description = await describe_image_bytes(contents)

        # ✅ Final API response
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