from fastapi import FastAPI, UploadFile, File


from teamB.src.integration import process_image

app = FastAPI()


@app.post("/cv/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        # ✅ Process image
        result = await process_image(file)

        # ✅ Return API contract
        # ✅ Return exact API contract
        # ✅ Return EXACT API contract (no extra fields)
        return result

    except Exception as e:
        return {
            "text": "",
            "labels": [],
            "description": "",
            "error": str(e)
        }
