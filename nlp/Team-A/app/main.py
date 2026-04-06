from fastapi import FastAPI
from app.api import summarize_api

app = FastAPI(title="AI NLP System")

app.include_router(summarize_api.router, prefix="/summarize", tags=["Summarization"])