from fastapi import FastAPI
from pydantic import BaseModel

from nlp.teamC.src.sentiment import (
    get_sentiment,
    smart_sentiment
)

from nlp.teamC.src.keywords import (
    get_keywords,
    smart_keywords
)

from nlp.teamC.src.summary import (
    summarize,
    smart_summary
)


app = FastAPI()


class TextRequest(BaseModel):
    text: str


@app.post("/nlp/analyze")
async def analyze_text(data: TextRequest):

    try:

        text = data.text

        # base results
        base_sentiment = get_sentiment(text)

        base_keywords = get_keywords(text)

        base_summary = summarize(text)

        # smart enhanced results
        sentiment_result = (
            smart_sentiment(text)
            or base_sentiment
        )

        keywords_result = (
            smart_keywords(text)
            or base_keywords
        )

        summary_result = (
            smart_summary(text)
            or base_summary
        )

        return {
            "sentiment": sentiment_result,
            "keywords": keywords_result,
            "summary": summary_result
        }

    except Exception:

        return {
            "sentiment": "neutral",
            "keywords": [],
            "summary": "processing error"
        }