# This module is done by Sri Harsha

from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
import webbrowser
import time
import threading


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Import only (no execution logic inside miniLM)
    import rag.Team_D.miniLM.miniLM as miniLM

    print("✅ Pipeline initialized")

    yield

    print("🔻 Shutting down...")


app = FastAPI(lifespan=lifespan)

# Import API routes
from rag.Team_D.FastAPI.api import app as api_app
app.router.routes = api_app.router.routes


# Optional: open browser safely
def open_browser():
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:8000/docs")


if __name__ == "__main__":
    threading.Thread(target=open_browser).start()

    uvicorn.run(
        "rag.Team_D.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )