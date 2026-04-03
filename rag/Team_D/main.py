import os
import sys
from fastapi import FastAPI
import uvicorn
import webbrowser
import time

# Add current directory to path for relative imports
sys.path.insert(0, os.path.dirname(__file__))

app = FastAPI()

from FastAPI.api import app as api_app 

app.router.routes = api_app.router.routes


if __name__ == "__main__":
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:8000/docs")
    uvicorn.run("main:app", reload=True)