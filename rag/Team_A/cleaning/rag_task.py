from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 1. List of words/phrases
keywords = [
    "sales increased",
    "sales decreased",
    "good profit",
    "loss",
    "breakeven"
]

# Request body model
class TextInput(BaseModel):
    text: str

# 2 & 3. Function inside API
@app.post("/match-keywords")
def match_keywords(input_data: TextInput):
    text = input_data.text.lower()
    matched_words = []

    # Loop through keywords and match
    for word in keywords:
        if word in text:
            matched_words.append(word)

    return {
        "input_text": input_data.text,
        "matched_keywords": matched_words
    }