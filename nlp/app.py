from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


from processor import process_text

app = FastAPI()

class NLPRequest(BaseModel):
    text: Optional[str] = None
    query: Optional[str] = None

@app.post("/nlp/analyze")
async def analyze_file(request: NLPRequest):

    try:
        
        # Only text
        if request.text:
            result = process_text(request.text)

        # Only query
        elif request.query:
            result = process_text(request.query)

        # Nothing provided
        else:
            return {
                "sentiment": "neutral",
                "summary": "No query or text provided",
                "keywords": [],
                "recommendations":[]
            }
        return result
    
    except Exception as e:
        print(f"NLP Error: {e}")
        
        return {
            "sentiment": "neutral",
            "summary": "processing error",
            "keywords": [],
            "recommendations":[]

        }

      