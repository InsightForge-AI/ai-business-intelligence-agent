from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Predefined phrases
phrases = [
    "worst delivery experience",
    "sales drop",
    "bad service",
    "late delivery"
]

# Input model
class Query(BaseModel):
    text: str

# Function to find matching phrases
def find_matches(input_text: str) -> List[str]:
    matches = []

    for phrase in phrases:
        if phrase.lower() in input_text.lower():
            matches.append(phrase)

    return matches

# Root API (for testing)
@app.get("/")
def home():
    return {"message": "Sentence Analysis API is running"}

# POST API
@app.post("/sentence-analysis")
def analyze_sentence(data: Query):
    matches = find_matches(data.text)

    return {
        "input": data.text,
        "matches": matches if matches else ["No match found"],
        "total_matches": len(matches)
    }