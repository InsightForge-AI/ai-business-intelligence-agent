import pandas as pd
import re
import os

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9 ]', '', text)
    return text


def preprocess_data():
    df = pd.read_json("rag\\Team_D\\Ecommerce_FAQ_Chatbot_dataset.json")
    df = pd.json_normalize(df['questions'])

    df = df.dropna()
    df = df.drop_duplicates()

    qa_pairs = df.apply(
        lambda row: {
            "question": clean_text(row['question']),
            "answer": clean_text(row['answer'])
        },
        axis=1
    ).tolist()

    return qa_pairs

qa_pairs = preprocess_data()