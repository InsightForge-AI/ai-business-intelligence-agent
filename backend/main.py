from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging_config import setup_logging

# start logging first
setup_logging()

from app.api.analyze import router


app = FastAPI(
    title="Backend Team",
    description="Integration Layer",
    version="1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)


@app.get("/")
def home():
    return {"status": "Backend running"}