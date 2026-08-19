# DocuMind RAG Microservice

## Overview

The RAG (Retrieval-Augmented Generation) microservice answers questions using document content.

## Features

- Document chunking
- Embedding generation
- Vector indexing
- Similarity retrieval
- Context formatting
- Question Answering using Qwen
- Structured JSON responses

## API

### POST

```
/rag/analyze
```

### Request

```json
{
    "query":"What is the total revenue?",
    "content":"Document text...",
    "metadata":{}
}
```

### Response

```json
{
    "module":"rag",
    "success":true,
    "answer":"The total revenue is $245.3 billion.",
    "sources":[
        "Chunk 1",
        "Chunk 3"
    ],
    "confidence":0.96,
    "message":"Question answered successfully."
}
```