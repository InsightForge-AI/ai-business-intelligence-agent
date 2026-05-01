from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Convert text → vector
def get_embedding(text: str):
    return model.encode(text)

# Compare two vectors
def get_similarity(vec1, vec2):
    return float(cosine_similarity([vec1], [vec2])[0][0])


# Test block
if __name__ == "__main__":
    text1 = "What is AI?"
    text2 = "Explain artificial intelligence"

    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)

    similarity = get_similarity(emb1, emb2)
    print("Similarity:", similarity)