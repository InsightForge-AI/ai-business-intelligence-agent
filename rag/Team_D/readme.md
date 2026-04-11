# Team D - RAG Service

## Overview

This is a FastAPI-based RAG (Retrieval-Augmented Generation) service.
It takes a user query and returns relevant answers from FAQ data using embeddings and vector search.

---

## Project Structure

```
rag/Team_D/
├── app/
│   ├── main.py
│   ├── routes/
│   ├── services/
│   └── core/
├── data/
├── tests/
└── README.md
```

---

## Setup

### Install dependencies

```
pip install -r requirements.txt
```

### Generate FAQ file (run once)

```python
from rag.Team_D.app.services.chunking import build_faq_file
build_faq_file()
```

---

## Run the Server

From project root:

```
python -m uvicorn rag.Team_D.app.main:app --reload
```

---

## API Usage

### Endpoint

```
POST /rag/query
```

### Request

```json
{
  "query": "Refund policy?"
}
```

### Response

```json
{
  "query": "Return policy",
  "answers": ["": our return policy generally covers products that are defective or damaged upon arrival damage due to improper use may not be eligible for a return please contact our customer support team for assistance",
    ": if a product was purchased as part of a bundle or set the return policy may vary please refer to the specific terms and conditions or contact our customer support team for further guidance",
    ": our return policy allows you to return products within 30 days of purchase for a full refund provided they are in their original condition and packaging please refer to our returns page for detailed instructions""]
}
```

---

## Testing

Run:

```
python rag/Team_D/Tests/testing.py
```

---

## Integration

### Backend (import)

```python
from rag.Team_D.app.services.retrieval import search
```

### API (recommended)

```python
import requests

requests.post(
    "http://127.0.0.1:8000/rag/query",
    json={"query": "return policy"}
)
```

---

## Notes

* Run from project root
* Use imports starting with `rag.Team_D...`
* Ensure `__init__.py` files are present
* Generate `faq.txt` before first run

---
