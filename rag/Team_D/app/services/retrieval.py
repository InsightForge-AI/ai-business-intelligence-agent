# This module is done by Rana Kumar and Chandrashekar

import chromadb

def create_collection(docs, embeddings):
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="rag_collection")

    ids = [str(i) for i in range(len(docs))]

    collection.add(
        documents=docs,
        embeddings=embeddings.tolist(),
        ids=ids
    )

    return collection


def normalize_query(query):
    """
    Normalize query by:
    - Converting to lowercase
    - Removing extra spaces
    - Removing duplicate consecutive words
    """
    # Convert to lowercase
    query = query.lower()
    
    # Remove leading/trailing spaces
    query = query.strip()
    
    # Normalize multiple spaces to single space
    query = " ".join(query.split())
    
    # Remove duplicate consecutive words
    words = query.split()
    normalized_words = []
    for word in words:
        if not normalized_words or normalized_words[-1] != word:
            normalized_words.append(word)
    
    return " ".join(normalized_words)


def calculate_relevance_score(top_distances):
    """
    Calculate if the result is relevant based on distance.
    Lower distance = higher relevance. 
    Threshold: 1.5 (allows more semantic flexibility for FAQ matches)
    """
    if not top_distances or len(top_distances) == 0:
        return False
    
    closest_distance = top_distances[0][0]
    # Lower threshold = stricter matching, higher threshold = more lenient
    # 1.5 is a good balance for FAQ semantic search
    return closest_distance < 1.5


def search(query, model, collection, top_k=3):
    # Default response (as per standard format)
    response = {
        "context": "",
        "source": None,
        "error": None
    }

    try:
        # 1. Handle empty query
        if not query or query.strip() == "":
            response["context"] = "no query provided"
            return response

        # 2. Normalize query (lowercase, remove extra spaces, deduplicate words)
        normalized_query = normalize_query(query)

        # 3. Encode normalized query
        query_embedding = model.encode([normalized_query]).tolist()

        # 4. Search in vector DB with distances
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            include=["distances"]
        )

        # 5. Handle no results
        if not results or "documents" not in results:
            response["context"] = "no data found"
            return response

        documents = results.get("documents", [[]])
        metadatas = results.get("metadatas", [[]])
        distances = results.get("distances", [[]])

        # 6. Check empty documents
        if not documents or not documents[0]:
            response["context"] = "no data found"
            return response

        # 7. Check relevance threshold
        if not calculate_relevance_score(distances):
            response["context"] = "no data found"
            return response

        # 8. Get top result
        response["context"] = documents[0][0]

        # 9. Handle source from metadata
        if metadatas and metadatas[0] and metadatas[0][0] is not None:
            response["source"] = metadatas[0][0].get("source", None)

        return response

    except Exception as e:
        response["error"] = str(e)
        return response

