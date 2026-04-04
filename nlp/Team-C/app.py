from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentiment import get_sentiment

from summary import summarize_text 
from keywords import extract_keywords

app = FastAPI()


# Define request body schema
class TextRequest(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "API is running"}

#when he comes here he shoud get the sentiment ,summary ,keywords 
@app.post("/nlp/analyze")
def analyze(data: TextRequest):
    try:
        text = data.text

        if not text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")

        sentiment = get_sentiment(text)
        summary = summarize_text(text) 
        keywords = extract_keywords(text)


        return {
            "sentiment": sentiment,
            "summary": summary,
            "keywords": keywords,
            "status": "success"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))