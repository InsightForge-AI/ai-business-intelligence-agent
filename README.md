# DocuMind — AI Document Intelligence Platform

DocuMind takes an uploaded document (PDF, DOCX, XLSX, CSV, or an image) and
runs it through a pipeline of specialized AI microservices — intent
routing, OCR/table extraction, NLP, statistical/ML analysis, and
retrieval-augmented Q&A — each optionally enhanced by its own local LLM,
served entirely offline via [Ollama](https://ollama.com). No document data
or LLM calls ever leave your machine.

## What it does

1. You upload a document through the web UI (or `POST /api/upload`).
2. The **agent** service reads your query and the document's metadata,
   asks a local LLM (Phi-3) to classify intent, and decides which
   analysis modules the request actually needs.
3. The relevant modules run in parallel:
   - **cv** — OCR, table/key-value extraction, chart detection (Llama 3)
   - **nlp** — summarization, keyword/entity extraction, sentiment, topics (Mistral)
   - **ml** — statistics, KPIs, trends, outlier and business-rule analysis (DeepSeek-R1)
   - **rag** — chunking, embedding, and question-answering over the document's content (Qwen 2.5)
4. The **backend** orchestrates all of it, aggregates each module's
   result into one response, and returns it — even if one module fails
   or its LLM is unreachable, since every module has a deterministic
   fallback (see [Known limitations](#known-limitations)).

## Architecture

```
                         ┌─────────────┐
   Browser ── /ui ──────▶│   backend    │── orchestrates ──┐
                         │  (port 8000) │                   │
                         └─────────────┘                    │
                                                              ▼
              ┌────────┬────────┬────────┬────────┬────────┐
              │ agent  │   ml   │  nlp   │   cv    │  rag   │
              │ :8001  │ :8002  │ :8003  │ :8004*  │ :8005* │
              │ Phi-3  │DeepSeek│Mistral │ Llama 3 │ Qwen2.5│
              └────────┴────────┴────────┴────────┴────────┘
                                    │
                              Ollama (local)
                          http://127.0.0.1:11434
```
<sub>* run.py starts rag on 8004 and cv on 8005.</sub>

Each service is an independent FastAPI app, started as its own OS
process by [run.py](run.py) — this mirrors how they'd actually be
deployed (separately, not as one monolith), and is also why each
service's tests must be run individually (see below).

## Getting started

**Requirements:** Python 3.12, and optionally [Ollama](https://ollama.com)
if you want real LLM-enhanced output instead of the deterministic
fallback results.

```bash
pip install -r requirements.txt
python run.py
```

This starts all 6 services. Open **http://127.0.0.1:8000/ui** for the
web UI, or **http://127.0.0.1:8000/docs** for the backend's interactive
API docs (each service also exposes its own `/docs` on its own port).

### Enabling real LLM output (optional)

Without Ollama running, every service still works — each one catches
the failed LLM call and falls back to its deterministic result (OCR
text as-is, statistical summary instead of an LLM-written one, etc.).
To get the actual LLM-enhanced output:

```bash
ollama pull phi3
ollama pull deepseek-r1:1.5b
ollama pull mistral
ollama pull llama3
ollama pull qwen2.5:3b
ollama pull nomic-embed-text   # used by rag for embeddings
```

Then just run `python run.py` as above — each service talks to
`http://127.0.0.1:11434` automatically once its model is present.

## Running tests

```bash
cd backend && pip install -r requirements.txt && python -m pytest tests/ -q
cd agent   && pip install -r requirements.txt && python -m pytest tests/ -q
cd ml      && pip install -r requirements.txt && python -m pytest tests/ -q
cd nlp     && pip install -r requirements.txt && python -m pytest tests/ -q
cd cv      && pip install -r requirements.txt && python -m pytest tests/ -q
cd rag     && pip install -r requirements.txt && python -m pytest tests/ -q
```

Run each service's suite **separately**, from that service's own
directory — see [Known limitations](#known-limitations) for why a single
combined `pytest` run from the repo root doesn't work.

## Known limitations

- **Services must be tested individually, not combined.** Several
  services use identically-named internal packages (`analysis`, `api`,
  `llm`). Each is completely safe as its own process — this only
  matters if you try to `pytest` more than one service in the same
  Python process at once, which `run.py` never does.
- **No CI pipeline yet** — tests are run manually per the commands above.
- **No authentication.** Anyone who can reach a service's port can use
  it. Fine for local/offline use; would need addressing before any
  multi-user or internet-facing deployment.
- **The web UI at `/ui` is intentionally minimal** — upload, list,
  analyze, download, delete. It's there to demonstrate the pipeline
  end-to-end, not as a polished product UI.
