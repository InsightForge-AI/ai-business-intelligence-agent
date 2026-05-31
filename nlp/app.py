from fastapi import FastAPI
from pydantic import BaseModel

from processor import process_text

app = FastAPI()

class NLPRequest(BaseModel):
    query: str 
    content: str

@app.post("/nlp/analyze")
async def analyze_file(request: NLPRequest):

    try:

    
        result = process_text(
            request.content
        )

        return result

    except Exception:

        return {
            "sentiment": "neutral",
            "summary": "processing error",
            "keywords": []
        }