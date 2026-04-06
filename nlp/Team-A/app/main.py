from fastapi import FastAPI
from app.api import summarize_api, sentiment_api, ke_api

app = FastAPI(title="AI NLP System")

app.include_router(summarize_api.router, prefix="/summarize", tags=["Summarization"])
app.include_router(sentiment_api.router, prefix="/sentiment", tags=["Sentiment"])
app.include_router(ke_api.router, prefix="/keywords", tags=["Keyword Extraction"])