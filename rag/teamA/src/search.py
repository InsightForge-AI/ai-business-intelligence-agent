docs = [
    "sales dropped",
    "bad delivery",
    "customer complaints increased",
    "revenue decreased last quarter",
    "shipping delays reported"
]

def search(query: str):
    query_words = query.lower().split()
    results = []
    
    for doc in docs:
        for word in query_words:
            if word in doc.lower():
                results.append(doc)
                break

    return results if results else "No relevant document found"

if __name__ == "__main__":
    print(search("delivery"))
    print(search("sales"))