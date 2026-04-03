
import os
import sys

# Add parent directory to path BEFORE importing modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from load_data.load_data import load_faq_data
from embedding.embedding import get_embeddings, model
from retrieval.retrievel import create_collection, search

# Load data
# Construct path relative to this file's location
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'faq.txt')
docs = load_faq_data(data_path)

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
