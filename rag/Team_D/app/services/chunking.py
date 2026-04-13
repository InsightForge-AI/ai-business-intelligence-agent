# This module is done by Manjula

from rag.Team_D.app.core.startup import preprocess_data
import os

def chunk_data(qa_pairs):
    chunks = []
    for qa in qa_pairs:
        chunk = f"Question: {qa['question']} Answer: {qa['answer']}"
        chunks.append(chunk)
    return chunks


def build_faq_file():
    print("📄 Building FAQ file...")

    qa_pairs = preprocess_data()
    chunks = chunk_data(qa_pairs)

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)

    faq_path = os.path.join(data_dir, 'faq.txt')

    with open(faq_path, 'w', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(chunk + '\n')

    print("✅ FAQ file created")

    return faq_path