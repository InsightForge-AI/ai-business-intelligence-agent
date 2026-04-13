import json
import os

def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "document.json")
    with open(file_path, "r", encoding="utf-8") as f:
        documents = json.load(f)
    return documents

if __name__ == "__main__":
    docs = load_data()
    for doc in docs:
        print(doc["title"], "->", doc["category"])