from fastapi import APIRouter
from pydantic import BaseModel

from app.preprocessing.loader import load_documents
from app.preprocessing.chunking import split_documents

from app.vectorstore.embeddings import load_embeddings
from app.vectorstore.chroma_db import create_vectorstore

from app.retrieval.retriever import retrieve_context

from app.llm.generator import generate_answer

router = APIRouter()

documents = load_documents()

chunks = split_documents(documents)

embeddings = load_embeddings()

db = create_vectorstore(
    chunks,
    embeddings
)

class QueryRequest(BaseModel):
    query: str


@router.post("/rag/query")
def rag(data: QueryRequest):

    try:

        docs = retrieve_context(
            db,
            data.query
        )

        context = "\n".join(
            [doc.page_content for doc in docs]
        )

        answer = generate_answer(
            data.query,
            docs
        )

        return {

            "query": data.query,

            "context": context,

            "answer": answer
        }

    except Exception as e:

        return {
            "error": str(e)
        }