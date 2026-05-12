from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Hospital RAG Assistant"
)

app.include_router(router)