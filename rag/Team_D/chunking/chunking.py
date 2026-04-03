import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from preprocessing.preprocessing import preprocess_data

def chunk_data(qa_pairs):
    chunks = []
    for qa in qa_pairs:
        chunk = "Question: {} Answer: {}".format(qa['question'], qa['answer'])
        chunks.append(chunk)
    return chunks


def build_faq_file():
    qa_pairs = preprocess_data()
    chunks = chunk_data(qa_pairs)

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)

    faq_path = os.path.join(data_dir, 'faq.txt')
    with open(faq_path, 'w', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(chunk + '\n')

    print(f'Chunks saved to {faq_path}')
    return faq_path