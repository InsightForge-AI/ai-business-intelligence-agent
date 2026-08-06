from fastapi import FastAPI

from teamB.src.sentiment import get_sentiment
from teamB.src.keywords import get_keywords
from teamB.src.summarizer import summarize

app = FastAPI()


@app.post("/nlp/analyze")
def analyze_text(data: dict):

    try:

        text = data.get("text", "")

        sentiment_result = get_sentiment(text)

        keywords_result = get_keywords(text)

        summary_result = summarize(text)

        return {
            "sentiment": sentiment_result,
            "summary": summary_result,
            "keywords": keywords_result,
        }

    except Exception as e:
        import logging
        logging.error(f"Error during NLP analysis: {e}", exc_info=True)

        # fallback response (never crash)

        return {
            "sentiment": "neutral",
            "summary": "processing error",
            "keywords": [],
        }