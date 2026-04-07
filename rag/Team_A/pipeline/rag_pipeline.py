from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os

# Load documents from JSON file
file_path = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned", "document_cleaned.json")
with open(file_path, "r", encoding="utf-8") as f:
    documents = json.load(f)

# Load model and encode documents
print("🔵 Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Model loaded")

contents = [doc["content"] for doc in documents]

print("🔵 Encoding documents...")
embeddings = model.encode(contents)
embeddings = np.array(embeddings).astype("float32")
print("✅ Encoding done")

# Build FAISS index
print("🔵 Building FAISS index...")
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)
print("✅ FAISS ready")


# 🔍 Search function
def search_pipeline(query: str, top_k: int = 3):
    query_embedding = model.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(documents):  # safety check
            doc = documents[idx]
            results.append({
                "title": doc["title"],
                "category": doc["category"],
                "content": doc["content"],
                "score": float(round(1 / (1 + distances[0][i]), 4))
            })

    return results


# 💾 Save results function
def save_results(query, results):
    output = {
        "query": query,
        "total_results": len(results),
        "results": results
    }

    save_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "cleaned", "pipeline_results.json"
    )

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, default=float)

    print("✅ Results saved to pipeline_results.json")


# 🚀 Main execution
if __name__ == "__main__":
    query = "sales report"
    results = search_pipeline(query)

    print("\n🔍 Search Results:\n")
    for r in results:
        print(f"{r['title']} -> {r['category']} | score: {round(r['score'], 4)}")

    save_results(query, results)