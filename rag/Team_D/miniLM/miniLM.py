from rag.Team_D.load_data.load_data import load_faq_data
from rag.Team_D.embedding.embedding import get_embeddings, model
from rag.Team_D.retrieval.retrievl import create_collection, search

# -----------------------------
# Load + initialize (runs once)
# -----------------------------

docs = load_faq_data(r"rag\Team_D\data\faq.txt")

embeddings = get_embeddings(docs)

collection = create_collection(docs, embeddings)

print("✅ RAG system initialized")


def run_query(query: str):
    results = search(query, model, collection)
    return results


if __name__ == "__main__":
    print("RAG system ready. Type your question\n")

    while True:
        query = input("You: ")

        if query.lower() == "exit":
            break

        results = run_query(query)

        print("\nAnswer:")
        for r in results:
            print("-", r)
        print()