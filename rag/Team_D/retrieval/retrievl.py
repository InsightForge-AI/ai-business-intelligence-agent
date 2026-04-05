import chromadb
from chromadb.config import Settings

# Create Chroma client (stores data locally)
client = chromadb.Client(Settings(persist_directory="./chroma_db"))

# Create collection
collection = client.get_or_create_collection(name="rag_collection")

#  Store vectors (instead of FAISS index.add)
def create_collection(docs, embeddings):
    ids = [str(i) for i in range(len(docs))]

    collection.add(
        documents=docs,
        embeddings=embeddings.tolist(),
        ids=ids
    )

    return collection


# ✅ Search function
def search(query, model, collection, top_k=3):
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    return results["documents"][0]






# Retrieval module placeholder

if __name__ == "__main__":
    print("Retrieval module initialized")
    
    # Print collection contents
    print("\n--- Collection Contents ---")
    collection_data = collection.get()
    
    print(f"Total items in collection: {len(collection_data['ids'])}")
    print(f"\nIDs: {collection_data['ids']}")
    print(f"\nDocuments: {collection_data['documents']}")
    
    if collection_data.get('metadatas'):
        print(f"\nMetadatas: {collection_data['metadatas']}")
    
    if collection_data.get('embeddings'):
        print(f"\nEmbeddings: {len(collection_data['embeddings'])} items")
    else:
        print("\nNo embeddings in collection yet")
