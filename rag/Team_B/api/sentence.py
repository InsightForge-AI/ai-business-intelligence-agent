from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# List of phrases
phrases = ["worst delivery experience", "sales drop"]

# Input model
class Query(BaseModel):
    text: str

# Function
def find_match(input_text: str):
    matches = []
    
    for phrase in phrases:
        if phrase.lower() in input_text.lower():
            matches.append(phrase)
    
    if matches:
        return matches
    else:
        return ["No match found"]

# POST API
@app.post("/sentence")
def check_sentence(data: Query):
    result = find_match(data.text)
    return {
        "input": data.text,
        "matches": result
    }