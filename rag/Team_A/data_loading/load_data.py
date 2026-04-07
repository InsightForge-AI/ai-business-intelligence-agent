from data.document import documents  

def load_data():
    return documents


if __name__ == "__main__":
    docs = load_data()
    for doc in docs:
        print(doc["title"], "->", doc["category"])