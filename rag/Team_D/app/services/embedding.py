# This module is done by Vineeth

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(docs):
    return model.encode(docs)