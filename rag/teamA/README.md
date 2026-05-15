# Hospital Intelligence RAG Assistant

## Project Overview

Hospital Intelligence RAG Assistant is a Retrieval-Augmented Generation (RAG) system developed as part of Sprint 4 of the AI Business Intelligence project.

The system retrieves relevant hospital-related information from internal documents and generates intelligent responses using a free Large Language Model (LLM).

This project demonstrates:
- Semantic Search
- Retrieval-Augmented Generation (RAG)
- Vector Embeddings
- FastAPI Integration
- Local LLM Inference

---

# Features

- Hospital FAQ retrieval
- Semantic similarity search
- Intelligent response generation
- FastAPI REST API
- ChromaDB vector storage
- Local free LLM using Ollama + Mistral
- Modular project structure
- GitHub-ready implementation

---

# Tech Stack

| Technology | Usage |
|---|---|
| Python | Backend |
| FastAPI | API Framework |
| LangChain | RAG Pipeline |
| ChromaDB | Vector Database |
| Sentence Transformers | Embeddings |
| Ollama | Local LLM Runtime |
| Mistral | Free LLM Model |

---

# Project Structure

```bash
rag/
└── teamA/
    │
    ├── app/
    │   ├── api/
    │   ├── data/
    │   ├── llm/
    │   ├── preprocessing/
    │   ├── retrieval/
    │   ├── vectorstore/
    │   └── main.py
    │
    ├── requirements.txt
    ├── .gitignore
    └── README.md
```

---

# Dataset

The project uses a hospital knowledge dataset containing:
- Appointment information
- Emergency services
- Insurance support
- Visiting hours
- Payment methods
- Online consultation details

Dataset format:

```python
{
    "question": "...",
    "answer": "..."
}
```

---

# RAG Workflow

```text
User Question
      ↓
Document Retrieval
      ↓
Semantic Search
      ↓
Relevant Context
      ↓
Mistral LLM
      ↓
Generated Response
```

---

# Installation

## 1. Clone Repository

```bash
git clone <repository-url>
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

---

## 3. Install Requirements

```bash
pip install -r requirements.txt
```

---

# Install Free LLM

Install Ollama:

https://ollama.com

Run Mistral model:

```bash
ollama run mistral
```

---

# Run FastAPI Server

```bash
uvicorn app.main:app --reload
```

---

# Swagger API Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

---

# API Endpoint

## POST `/rag/query`

### Request

```json
{
  "query": "How can I book appointment?"
}
```

---

### Response

```json
{
  "query": "How can I book appointment?",
  "answer": "Appointments can be booked through the hospital website or reception desk."
}
```

---

# Example Questions

- How can I book appointment?
- Does hospital provide emergency services?
- What payment methods are accepted?
- Can I consult doctors online?
- Does hospital support insurance?

---

# Key Concepts Used

- Retrieval-Augmented Generation (RAG)
- Embeddings
- Semantic Search
- Vector Database
- Context Retrieval
- Prompt Engineering
- LLM Integration

---

# Sprint 4 Goals Achieved

- Retrieve answers from documents
- Semantic document search
- Best result retrieval
- AI-generated responses
- FastAPI integration
- Modular architecture

---

# Future Improvements

- PDF document support
- Chat history memory
- Multi-document retrieval
- Frontend integration
- Voice assistant support
- Authentication system

---

# Developed For

Sprint 4 — Smart Intelligence Phase

AI Business Intelligence System Version 2.0