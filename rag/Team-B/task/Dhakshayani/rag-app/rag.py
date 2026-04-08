from fastapi import FastAPI

# Updated LangChain imports (latest)
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

app = FastAPI()

#  Step 1: Load TXT file
loader = TextLoader("data/ai_project_txt.txt")   # make sure file is inside data folder
documents = loader.load()

#  Step 2: Split text
splitter = CharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)
docs = splitter.split_documents(documents)

#  Step 3: FREE Embeddings 
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

#  Step 4: Vector DB (FAISS)
db = FAISS.from_documents(docs, embeddings)

#  Step 5: API Endpoint
@app.get("/ask")
def ask_question(query: str):
    results = db.similarity_search(query, k=2)

    return {
        "question": query,
        "answer": results[0].page_content
    }

#  Root API
@app.get("/")
def home():
    return {"message": "RAG API running sucessfully"}