from fastapi import APIRouter, UploadFile, File
import pandas as pd
import io

from core.summarization.summarize import generate_insights, get_summary

router = APIRouter()


@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        df = pd.read_csv(io.BytesIO(contents), encoding='latin1')

        insights = generate_insights(df)
        summary = get_summary(insights)

        return {
            "filename": file.filename,
            "rows": len(df),
            "columns": list(df.columns),
            "insights": insights,
            "summary": summary
        }

    except Exception as e:
        return {"error": str(e)}