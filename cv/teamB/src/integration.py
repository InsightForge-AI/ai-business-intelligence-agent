from cv.teamB.src.ocr import extract_text
from cv.teamB.src.labeling import analyze_image
from cv.teamB.src.description import run_description

import shutil


async def process_image(file):
    try:
        # ✅ Save uploaded image temporarily
        file_path = f"temp_{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ✅ OCR
        text = extract_text(file_path)

        # ✅ Reset file pointer before next read
        await file.seek(0)

        # ✅ Labeling using LLaVA
        labels = await analyze_image(file)

        # ✅ Reset again before description
        await file.seek(0)

        # ✅ Description using LLaVA
        description = await run_description(file)

        # ✅ Final API response
        return {
            "text": text,
            "labels": labels,
            "description": description
        }

    except Exception as e:
        return {
            "text": "",
            "labels": [],
            "description": "",
            "error": str(e)
        }