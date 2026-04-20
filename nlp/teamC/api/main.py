from fastapi import FastAPI
from pydantic import BaseModel

from nlp.teamC.src.sentiment import get_sentiment
from nlp.teamC.src.summary import summarize_text
from nlp.teamC.src.keywords import extract_keywords

app = FastAPI()

class TextRequest(BaseModel):
    text: str


@app.post("/nlp/analyze")
def analyze(data: TextRequest):
    text = data.text.strip()

    sentiment = get_sentiment(text)
    summary = summarize_text(text)
    keywords = extract_keywords(text)

    return {
        "sentiment": sentiment,
        "summary": summary,
        "keywords": keywords
    }