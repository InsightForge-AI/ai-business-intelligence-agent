import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from preprocessing.preprocessing import preprocess_data

qa_pairs = preprocess_data()

def chunk_data(qa_pairs):
    chunks = []

    for qa in qa_pairs:
        # Each Q&A = one chunk (best for FAQ)
        chunk = "Question: {} Answer: {}".format(qa['question'], qa['answer'])
        chunks.append(chunk)

    return chunks

chunks = chunk_data(qa_pairs)

# Create folder if not exists
os.makedirs("rag/Team_D/data", exist_ok=True)

# Save chunks to file
with open("rag/Team_D/data/faq.txt", "w", encoding="utf-8") as f:
    for chunk in chunks:
        f.write(chunk + "\n")
print("Chunks saved to data/faq.txt")

