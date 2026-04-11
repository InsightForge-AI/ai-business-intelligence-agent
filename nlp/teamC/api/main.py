from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.sentiment import get_sentiment
from src.summary import summarize_text
from src.keywords import extract_keywords

app = FastAPI()


class TextRequest(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "API is running"}


@app.post("/nlp/analyse")
def analyze(data: TextRequest):
    text = data.text

    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    sentiment = get_sentiment(text)
    summary = summarize_text(text)
    keywords = extract_keywords(text)

    return {
        "sentiment": sentiment,
        "summary": summary,
        "keywords": keywords
    }