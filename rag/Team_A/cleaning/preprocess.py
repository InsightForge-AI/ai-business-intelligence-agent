import json
import os
import re

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[!?.:,&()\-]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_documents(documents):
    cleaned = []
    for doc in documents:
        cleaned.append({
            "title": doc["title"],
            "content": preprocess_text(doc["content"]),
            "category": doc["category"]
        })
    return cleaned

if __name__ == "__main__":
    # Load raw data
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "document.json")
    with open(file_path, "r", encoding="utf-8") as f:
        documents = json.load(f)

    # Clean data
    cleaned_docs = preprocess_documents(documents)

    # Save to cleaned folder
    output_path = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned", "document_cleaned.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_docs, f, indent=4)

    print("Cleaning done! Saved to data/cleaned/document_cleaned.json")
    for doc in cleaned_docs:
        print(doc["title"], "->", doc["content"][:60])