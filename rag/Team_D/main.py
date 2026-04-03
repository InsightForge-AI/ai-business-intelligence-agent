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

from preprocessing.preprocessing import preprocess_data
from chunking.chunking import build_faq_file


def run_pipeline():
    print('Running preprocessing...')
    qa_pairs = preprocess_data()
    print(f'Loaded {len(qa_pairs)} QA pairs')

    print('Running chunking...')
    faq_path = build_faq_file()
    print(f'FAQ file created: {faq_path}')


if __name__ == "__main__":
    run_pipeline()
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:8000/docs")
    uvicorn.run("main:app", reload=True)