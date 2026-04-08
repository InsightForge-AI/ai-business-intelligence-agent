from fastapi import FastAPI
from app.api import summarize_api, sentiment_api, ke_api

app = FastAPI(title="AI NLP System")

app.include_router(summarize_api.router, prefix="/nlp", tags=["Summarization"])
app.include_router(sentiment_api.router, prefix="/nlp", tags=["Sentiment"])
app.include_router(ke_api.router, prefix="/nlp", tags=["Keyword Extraction"])