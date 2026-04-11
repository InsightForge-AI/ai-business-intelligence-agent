# This module is done by Sri Harsha

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routes.rag_routes import router
from app.core.startup import initialize_system


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    collection = initialize_system()

    import app.routes.rag_routes as routes
    routes.collection = collection

    yield

    # Shutdown (optional)
    print("Shutting down...")


app = FastAPI(title="Team D RAG Service", lifespan=lifespan)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "RAG API running"}