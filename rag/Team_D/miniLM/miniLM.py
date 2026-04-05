from rag.Team_D.load_data.load_data import load_faq_data
from rag.Team_D.embedding.embedding import get_embeddings, model
from rag.Team_D.retrieval.retrievl import create_collection, search

# Load data
docs = load_faq_data(r"rag\Team_D\data\faq.txt")

# Create embeddings
embeddings = get_embeddings(docs)

# Store in ChromaDB
collection = create_collection(docs, embeddings)

print("RAG system ready. Type your question\n")

while True:
    query = input("You: ")

    if query.lower() == "exit":
        break

    results = search(query, model, collection)

    print("\nAnswer:")
    for r in results:
        print("-", r)
    print()

# miniLM module placeholder

if __name__ == "__main__":
    print("miniLM module initialized")
