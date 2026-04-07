from fastapi import APIRouter
from pydantic import BaseModel

from core.sentiment_analysis.sentiment import get_sentiment

router = APIRouter()


# Request Schema
class TextInput(BaseModel):
    text: str


@router.post("/sentiment")
async def sentiment_api(data: TextInput):
    result = get_sentiment(data.text)

    return {
        "input": data.text,
        "sentiment": result
    }