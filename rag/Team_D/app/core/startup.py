# This module is done by Sanghavi

import pandas as pd
import re
import os

from rag.Team_D.app.services.embedding import get_embeddings
from rag.Team_D.app.services.retrieval import create_collection


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9 ]', '', text)
    return text


def preprocess_data():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    json_path = os.path.join(base_dir, 'data', 'Ecommerce_FAQ_Chatbot_dataset.json')

    df = pd.read_json(json_path)
    df = pd.json_normalize(df['questions'])

    df = df.dropna()
    df = df.drop_duplicates()

    qa_pairs = df.apply(
        lambda row: {
            'question': clean_text(row['question']),
            'answer': clean_text(row['answer'])
        },
        axis=1
    ).tolist()

    return qa_pairs


def load_faq_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().lower()

    parts = text.split("question")

    docs = []
    for part in parts:
        if "answer" in part:
            qa = part.split("answer")
            if len(qa) > 1:
                answer = qa[1].strip()
                docs.append(answer)

    return docs


def initialize_system():
    print("🚀 Initializing RAG system...")

    qa_pairs = preprocess_data()
    questions = [qa['question'] for qa in qa_pairs]
    answers = [qa['answer'] for qa in qa_pairs]

    embeddings = get_embeddings(questions)
    metadatas = [{"answer": ans} for ans in answers]
    collection = create_collection(questions, embeddings, metadatas)

    print("✅ RAG system ready")

    return collection