# retriever.py
# ============================================================
# Core RAG Logic — Team A
# Nandhitha & Naryani
# ============================================================

import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K           = 3
MIN_SIMILARITY  = 0.25

# ---------------------------------------------------------------------------
# DOCUMENT STORE
# ---------------------------------------------------------------------------
DOCUMENTS = [
    "sales dropped due to bad delivery",
    "customers complaining about late delivery",
    "delivery delay caused customer dissatisfaction",
    "revenue decreased last quarter",
    "shipping delays reported",
]

# ---------------------------------------------------------------------------
# LOAD MODEL & INDEX DOCUMENTS
# ---------------------------------------------------------------------------
print("[retriever] Loading embedding model...")
_model = SentenceTransformer(EMBEDDING_MODEL)

print("[retriever] Indexing documents...")
_doc_embeddings = _model.encode(DOCUMENTS, convert_to_numpy=True)
print(f"[retriever] Indexed {len(DOCUMENTS)} documents.")

# ---------------------------------------------------------------------------
# RETRIEVE
# ---------------------------------------------------------------------------
def retrieve(query: str, top_k: int = TOP_K) -> list[dict]:
    """
    Embed query → cosine similarity → return top-k chunks
    """
    if not query or not query.strip():
        return []

    query_embedding = _model.encode([query.strip()], convert_to_numpy=True)
    scores = cosine_similarity(query_embedding, _doc_embeddings)[0]
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []
    for idx in top_indices:
        if scores[idx] >= MIN_SIMILARITY:
            results.append({
                "chunk": DOCUMENTS[idx],
                "score": round(float(scores[idx]), 4)
            })
    return results

# ---------------------------------------------------------------------------
# BUILD CONTEXT
# ---------------------------------------------------------------------------
def build_context(chunks: list[dict]) -> str:
    """
    Format retrieved chunks into LLM-ready context block
    """
    if not chunks:
        return "No relevant context found."

    lines = []
    for i, c in enumerate(chunks, 1):
        lines.append(f"[{i}] {c['chunk']}  (relevance: {c['score']})")
    return "\n".join(lines)

# ---------------------------------------------------------------------------
# FULL RAG PIPELINE
# ---------------------------------------------------------------------------
def rag_answer(query: str) -> dict:
    """
    Full pipeline: query → retrieve → context → LLM answer
    """
    chunks  = retrieve(query)
    context = build_context(chunks)

    # ── Wire your LLM here ───────────────────────────────────
    # prompt = f"""
    # Use the context below to answer the question.
    # Context:
    # {context}
    # Question: {query}
    # Answer:
    # """
    # answer = your_llm_client.complete(prompt)
    # ─────────────────────────────────────────────────────────

    answer = f"[LLM STUB] Based on context:\n{context}"

    return {
        "query"  : query,
        "chunks" : chunks,
        "context": context,
        "answer" : answer,
    }

# ---------------------------------------------------------------------------
# TESTS — Nandhitha & Naryani
# ---------------------------------------------------------------------------
def run_tests():
    print("\n" + "="*60)
    print("RUNNING ALL TESTS")
    print("="*60)

    # ── Nandhitha: Core retrieval tests ──────────────────────
    print("\n[ Nandhitha — Retrieval Tests ]\n")

    retrieval_tests = [
        ("Why did sales go down?",             True),   # should find results
        ("Are there delivery problems?",        True),   # should find results
        ("What are customers unhappy about?",   True),   # should find results
        ("random unrelated topic",              False),  # should find nothing
        ("",                                   False),  # empty — should return []
        ("   ",                                False),  # whitespace — should return []
    ]

    for query, expect_results in retrieval_tests:
        result  = retrieve(query)
        passed  = (len(result) > 0) == expect_results
        status  = "PASS" if passed else "FAIL"
        print(f"  [{status}] Query: {repr(query)}")
        if result:
            for r in result:
                print(f"         → {r['chunk']}  (score: {r['score']})")
        else:
            print(f"         → No results returned")

    # ── Naryani: Edge case & pipeline tests ──────────────────
    print("\n[ Naryani — Edge Case & Pipeline Tests ]\n")

    edge_tests = [
        "LATE DELIVERY",                    # uppercase
        "late delivery!!!",                 # special characters
        "customers revenue delivery",       # multiple keywords
        "shipment",                         # single word
        None,                               # None input — must not crash
    ]

    for query in edge_tests:
        try:
            result = rag_answer(query) if query is not None else rag_answer("")
            status = "PASS"
            chunks_found = len(result["chunks"])
        except Exception as e:
            status = "FAIL"
            chunks_found = 0
            print(f"  [FAIL] Query: {repr(query)} → ERROR: {e}")
            continue

        print(f"  [{status}] Query: {repr(query)} → {chunks_found} chunk(s) retrieved")

    print("\n" + "="*60)
    print("ALL TESTS COMPLETE")
    print("="*60)

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Run all tests
    run_tests()

    # Quick demo
    print("\n[ DEMO — Full RAG Pipeline ]\n")
    demo_query = "Why are customers complaining?"
    output = rag_answer(demo_query)
    print(f"Query   : {output['query']}")
    print(f"Context :\n{output['context']}")
    print(f"Answer  : {output['answer']}")