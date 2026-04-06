from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

lst = ["practical", "impact"]

class TextRequest(BaseModel):
    text: str

@app.post("/search")
def retrieve(data: TextRequest):
    words = data.text.lower().split()
    matched_words = [word for word in words if word in lst]
    return {"words": matched_words} 