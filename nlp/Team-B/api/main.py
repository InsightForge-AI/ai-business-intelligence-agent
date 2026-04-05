from fastapi import FastAPI
import sys
import os
import json

# Add parent directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Import modules
from sentiment.sentiment import get_sentiment
from keywords.keywords import get_keywords
from Summary.summarizer import summarize

app = FastAPI()


# Home Route
@app.get("/")
def home():
    return {"message": "Team-B NLP API Running Successfully"}


# Analyze Text from Request
@app.post("/analyze")
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
        "keywords": keywords_result,
        "summary": summary_result
    }


# Analyze Text from JSON File
@app.get("/analyze-from-file")
def analyze_from_file():

    file_path = "../Data/texts.json"

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