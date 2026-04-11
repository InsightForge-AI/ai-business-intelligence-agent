from fastapi import FastAPI

# Import service modules
from src.sentiment import get_sentiment
from src.keywords import get_keywords
from src.summarizer import summarize

app = FastAPI()


# Analyze Text from Request
@app.post("/nlp/analyze")
def analyze_text(data: dict):

    text = data.get("text")

    if not text:
        return {"error": "No text provided"}

    sentiment_result = get_sentiment(text)

    keywords_result = get_keywords(text)

    summary_result = summarize(text)

    return {
        "sentiment": sentiment_result,
        "summary": summary_result,
        "keywords": keywords_result,
    }
