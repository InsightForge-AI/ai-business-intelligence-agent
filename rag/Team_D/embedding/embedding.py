from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to generate embeddings
def get_embeddings(docs):
    return model.encode(docs)


# Embedding module placeholder

if __name__ == "__main__":
    print("Embedding module initialized")
