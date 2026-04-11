# NLP (Team-B)

## Modules Overview

- Sentiment Analysis
- Keyword Extraction
- Text Summarization

The API processes user-provided text or reads text data from a JSON file and returns structured analysis results.


##  Features

- Sentiment detection (Positive, Negative, Neutral)
- Keyword extraction (Top important words)
- Text summarization (First important sentences)
- JSON file input support
- Modular service-based architecture


##  Project Structure
TEAM-B/
│
├── services/
| ├── __init__.py
│ ├── keywords/
│ │ ├── __init__.py
│ │ └── keywords.py
│ │
│ ├── sentiment/
│ │ ├── __init__.py
│ │ └── sentiment.py
│ │
│ └── summary/
│ ├── __init__.py
│ ├── preprocess.py
│ ├── summarizer.py
│ └── utils.py
│
├── data/
│ └── texts.json
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md

## Install dependencies

pip install -r requirements.txt

## API Endpoints 
1️⃣ Analyze Text
POST /nlp/analyze

Input:
{
  "text": "This product is very good and useful."
}

Output:
{
  "text": "This product is very good and useful.",
  "sentiment": "positive",
  "keywords": ["product", "good", "useful"],
  "summary": "This product is very good."
}

2️⃣ Analyze Text from File

GET /analyze-from-file
Input : Reads text data from data/texts.json
Output : Returns analysis results for each entry

## 📌 Requirements

Dependencies are listed in : requirements.txt

1.fastapi
2.uvicorn

