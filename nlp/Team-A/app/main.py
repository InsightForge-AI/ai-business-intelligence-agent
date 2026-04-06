from fastapi import FastAPI
from app.api import summarize_api, sentiment_api

app = FastAPI(title="AI NLP System")

# Routers
app.include_router(summarize_api.router, prefix="/summarize", tags=["Summarization"])
app.include_router(sentiment_api.router, prefix="/sentiment", tags=["Sentiment"])