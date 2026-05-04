from fastapi import FastAPI

#importing stable functions
from nlp.teamC.src.sentiment import get_sentiment
from nlp.teamC.src.keywords import get_keywords
from nlp.teamC.src.summarizer import summarize

#importing smart functions
from nlp.teamC.src.sentiment import smart_sentiment
from nlp.teamC.src.keywords import smart_keywords
from nlp.teamC.src.summarizer import smart_summary


app = FastAPI()


@app.post("/nlp/analyze")
def analyze_text(data: dict):

    try:

        text = data.get("text", "")

        #Always compute stable results first

        base_sentiment = get_sentiment(text)

        base_keywords = get_keywords(text)

        base_summary = summarize(text)

        #Smart enhancement

        sentiment_result = smart_sentiment(text) or base_sentiment

        keywords_result = smart_keywords(text) or base_keywords

        summary_result = smart_summary(text) or base_summary

       

        return {
            "sentiment": sentiment_result,
            "summary": summary_result,
            "keywords": keywords_result,
        
        }

    except Exception:

        # fallback response (never crash)

        return {
            "sentiment": "neutral",
            "summary": "processing error",
            "keywords": [],


        }