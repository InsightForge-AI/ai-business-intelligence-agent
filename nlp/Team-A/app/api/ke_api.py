from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from core.keyword_extraction.ke import extract_keywords

router = APIRouter()


class TextRequest(BaseModel):
    text: str
    top_k: Optional[int] = None


@router.post("/extract-keywords")
def get_keywords(data: TextRequest):
    keywords = extract_keywords(data.text, data.top_k)

    return {
        "keywords": keywords,
        "count": len(keywords)
    }