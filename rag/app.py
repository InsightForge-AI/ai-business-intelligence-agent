from fastapi import FastAPI
from pydantic import BaseModel

import ollama

from ingest import (
    build_document_index
)

from retriever import (
    retrieve_context
)

from prompts import (
    build_prompt
)

app = FastAPI()

INDEX = None
CHUNKS = None


class IngestRequest(BaseModel):
    document_text: str


class QueryRequest(BaseModel):
    question: str


@app.post("/rag/ingest")
def ingest_document(
    request: IngestRequest
):

    global INDEX
    global CHUNKS

    INDEX, CHUNKS = (
        build_document_index(
            request.document_text
        )
    )

    return {
        "message":
        "Document indexed successfully",
        "chunks":
        len(CHUNKS)
    }


def generate_answer(
    question,
    context
):

    if not context.strip():

        return (
            "Information not found"
        )

    prompt = build_prompt(
        question,
        context
    )

    response = ollama.chat(
        model="qwen2.5:1.5b",
        messages=[
            {
                "role": "system",
                "content":
                "Answer only from the supplied context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response[
        "message"
    ]["content"]


def calculate_confidence(
    retrieved_chunks
):

    if not retrieved_chunks:
        return 0.0

    avg_score = sum(
        chunk["score"]
        for chunk in retrieved_chunks
    ) / len(retrieved_chunks)

    return round(
        avg_score,
        4
    )


@app.post("/rag/query")
def query_document(
    request: QueryRequest
):

    global INDEX
    global CHUNKS

    if INDEX is None:

        return {
            "error":
            "No document indexed."
        }

    result = retrieve_context(
        request.question,
        INDEX,
        CHUNKS
    )

    answer = generate_answer(
        request.question,
        result["context"]
    )

    confidence = (
        calculate_confidence(
            result[
                "retrieved_chunks"
            ]
        )
    )

    return {

        "question":
        request.question,

        "retrieved_chunks":
        [
            chunk["content"]
            for chunk in result[
                "retrieved_chunks"
            ]
        ],

        "answer":
        answer,

        "confidence":
        confidence
    }