# Install (only needed in Colab once)


# Import libraries
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Import dataset
df = pd.read_csv('Restaurant_Reviews.tsv', delimiter='\t')
df.head()

# Initialize analyzer (only once)
analyzer = SentimentIntensityAnalyzer()

# ✅ Generic function (DATA-INDEPENDENT)
from fastapi import FastAPI
from pydantic import BaseModel
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = FastAPI()

analyzer = SentimentIntensityAnalyzer()

# Request body schema
class TextInput(BaseModel):
    text: str

def get_sentiment(text: str) -> str:
    if not isinstance(text, str):
        return "neutral"
    
    score = analyzer.polarity_scores(text)
    compound = score['compound']

    if compound >= 0.05:
        return "positive"
    elif compound <= -0.05:
        return "negative"
    else:
        return "neutral"

# POST API
@app.post("/sentiment")
async def sentiment_api(data: TextInput):
    result = get_sentiment(data.text)
    return {
        "input": data.text,
        "sentiment": result
    }