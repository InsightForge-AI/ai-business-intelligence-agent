# Load data module placeholder

import os

def load_faq_data(file_path):
    # Read file
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().lower()

    # Process text
    parts = text.split("question")

    docs = []
    for part in parts:
        if "answer" in part:
            # split question and answer
            qa = part.split("answer")

            if len(qa) > 1:
                answer = qa[1].strip()   # ONLY ANSWER
                docs.append(answer)
    print(docs)
    return docs

if __name__ == "__main__":
    print("Load data module initialized")
    # Construct relative path to faq.txt
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    faq_path = os.path.join(base_dir, 'data', 'faq.txt')
    load_faq_data(faq_path)
