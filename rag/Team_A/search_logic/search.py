import json
import os

def load_cleaned_data():
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned", "document_cleaned.json")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def search(query, data):
    query_words = query.lower().split()
    results = []

    for item in data:
        doc_words = item["content"].lower().split()
        score = len(set(query_words) & set(doc_words))

        if score > 0:
            results.append((score, item))

    results.sort(reverse=True, key=lambda x: x[0])

    return [doc for _, doc in results[:3]]

if __name__ == "__main__":
    data = load_cleaned_data()
    results = search("sales report", data)
    for doc in results:
        print(doc["title"], "->", doc["category"])