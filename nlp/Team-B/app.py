from fastapi import FastAPI
import sys
import os
import json

# Add parent directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Import modules
from services.sentiment.sentiment import get_sentiment
from services.keywords.keywords import get_keywords
from services.summary.summarizer import summarize

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
        "text": text,
        "sentiment": sentiment_result,
        "summary": summary_result,
        "keywords": keywords_result,
    }


# Analyze Text from JSON File
@app.get("/analyze-from-file")
def analyze_from_file():

    file_path = os.path.join(BASE_DIR, "data", "texts.json")

    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        results = []

        for item in data:

            text = item.get("text", "")

            sentiment_result = get_sentiment(text)

            keywords_result = get_keywords(text)

            summary_result = summarize(text)

            results.append({
                "id": item.get("id"),
                "text": text,
                "sentiment": sentiment_result,
                "keywords": keywords_result,
                "summary": summary_result
            })

        return results

    except Exception as e:
        return {"error": str(e)}