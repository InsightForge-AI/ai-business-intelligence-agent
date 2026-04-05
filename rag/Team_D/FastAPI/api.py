# FastAPI entrypoint placeholder

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Team_D API running"}
