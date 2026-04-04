from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Predefined phrases (business-related patterns)
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
def find_matches(input_text: str):
    matches = []

    for phrase in phrases:
        if phrase.lower() in input_text.lower():
            matches.append(phrase)

    if matches:
        return matches
    else:
        return ["No match found"]

# POST API
@app.post("/sentence-analysis")
def analyze_sentence(data: Query):
    result = find_matches(data.text)

    return {
        "input": data.text,
        "matches": result,
        "total_matches": len(result) if result != ["No match found"] else 0
    }

