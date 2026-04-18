from fastapi import FastAPI
from app.api.analyze import router

app = FastAPI(
    title = "Backend Team",
    description="Integration Layer",
    version="1.0"
)

app.include_router(router)

@app.get("/")
def home():
    return {"status":"Backend running"}