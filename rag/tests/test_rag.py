"""
Tests for the RAG service's deterministic pipeline (chunker,
vector_store, retriever, reranker). These test files were previously
empty stubs (0 bytes) -- this is the first real coverage for this
module.

Qwen/LLM-backed pieces (llm/*, embeddings.py's actual model calls) are
not covered here since no Ollama runtime is available in this
environment.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # rag/

from analysis.chunker import chunk_document
from analysis.vector_store import build_index
from analysis.retriever import cosine_similarity, retrieve_chunks
from analysis.reranker import rerank_chunks


class TestChunker:

    def test_empty_text_returns_no_chunks(self):
        assert chunk_document("") == []
        assert chunk_document("   ") == []
        assert chunk_document(None) == []

    def test_short_paragraph_becomes_one_chunk(self):
        chunks = chunk_document("A short paragraph about revenue.")
        assert len(chunks) == 1
        assert chunks[0]["chunk_id"] == 1

    def test_multiple_paragraphs_become_multiple_chunks(self):
        text = "First paragraph here.\nSecond paragraph here.\nThird one."
        chunks = chunk_document(text)
        assert len(chunks) == 3
        assert [c["chunk_id"] for c in chunks] == [1, 2, 3]

    def test_long_paragraph_is_split_with_overlap(self):
        # CHUNK_SIZE=200, CHUNK_OVERLAP=50 (rag/utils/constants.py)
        text = " ".join(f"word{i}" for i in range(450))
        chunks = chunk_document(text)
        assert len(chunks) > 1
        # Consecutive chunks should overlap by CHUNK_OVERLAP words.
        assert chunks[1]["start_word"] == chunks[0]["end_word"] - 50

    def test_blank_lines_are_skipped(self):
        text = "First.\n\n\nSecond."
        chunks = chunk_document(text)
        assert len(chunks) == 2


class TestVectorStoreIsRequestScoped:
    """
    Regression suite for a critical concurrency bug: vector_store.py
    used to keep a single module-level global VECTOR_STORE list that
    build_index() cleared and repopulated on every call, and
    retriever.retrieve_chunks() read via get_index(). Reproduced
    directly: build an index for "document A", then build an index for
    "document B" (simulating a concurrent request -- reachable in
    practice because services/rag_service.run_analysis() awaits
    generate_embeddings() between build_index() and retrieve_chunks(),
    which is exactly where the event loop can switch to another
    request), then query "for document A" -- the old code returned
    document B's content. Fixed by having build_index() return a plain
    list instead of mutating shared state, with retrieve_chunks() now
    taking that index as an explicit parameter.
    """

    def test_build_index_does_not_share_state_between_calls(self):
        index_a = build_index(
            chunks=[{"chunk_id": 1, "text": "Document A: confidential salary data"}],
            embeddings=[[1.0, 0.0]],
        )
        # A second, unrelated build_index() call -- simulating another
        # document/request -- must not affect index_a's own list.
        build_index(
            chunks=[{"chunk_id": 2, "text": "Document B: unrelated notes"}],
            embeddings=[[1.0, 0.0]],
        )

        assert len(index_a) == 1
        assert index_a[0]["text"] == "Document A: confidential salary data"

    def test_retrieve_chunks_only_sees_its_own_index(self):
        index_a = build_index(
            chunks=[{"chunk_id": 1, "text": "Document A content"}],
            embeddings=[[1.0, 0.0]],
        )
        index_b = build_index(
            chunks=[{"chunk_id": 2, "text": "Document B content"}],
            embeddings=[[1.0, 0.0]],
        )

        results_a = retrieve_chunks(index=index_a, query_embedding=[1.0, 0.0])
        results_b = retrieve_chunks(index=index_b, query_embedding=[1.0, 0.0])

        assert results_a[0]["text"] == "Document A content"
        assert results_b[0]["text"] == "Document B content"

    def test_chunks_without_embeddings_are_skipped(self):
        index = build_index(
            chunks=[
                {"chunk_id": 1, "text": "has embedding"},
                {"chunk_id": 2, "text": "no embedding"},
            ],
            embeddings=[[1.0, 0.0], []],
        )
        assert len(index) == 1
        assert index[0]["text"] == "has embedding"


class TestCosineSimilarity:

    def test_identical_vectors_score_one(self):
        assert cosine_similarity([1.0, 0.0], [1.0, 0.0]) == pytest.approx(1.0)

    def test_orthogonal_vectors_score_zero(self):
        assert cosine_similarity([1.0, 0.0], [0.0, 1.0]) == pytest.approx(0.0)

    def test_empty_vector_returns_zero_not_crash(self):
        assert cosine_similarity([], [1.0]) == 0.0
        assert cosine_similarity([1.0], []) == 0.0

    def test_zero_vector_returns_zero_not_divide_by_zero(self):
        assert cosine_similarity([0.0, 0.0], [1.0, 0.0]) == 0.0


class TestRetrieveChunks:

    def test_empty_index_returns_no_chunks(self):
        assert retrieve_chunks(index=[], query_embedding=[1.0, 0.0]) == []

    def test_results_sorted_by_similarity_descending(self):
        index = build_index(
            chunks=[
                {"chunk_id": 1, "text": "weak match"},
                {"chunk_id": 2, "text": "strong match"},
            ],
            embeddings=[[0.1, 0.9], [1.0, 0.0]],
        )
        results = retrieve_chunks(index=index, query_embedding=[1.0, 0.0])
        assert results[0]["text"] == "strong match"

    def test_respects_top_k(self):
        index = build_index(
            chunks=[{"chunk_id": i, "text": f"chunk {i}"} for i in range(10)],
            embeddings=[[1.0, 0.0]] * 10,
        )
        results = retrieve_chunks(index=index, query_embedding=[1.0, 0.0], top_k=3)
        assert len(results) == 3


class TestRerankChunks:

    def test_empty_input_returns_empty_list(self):
        assert rerank_chunks([]) == []

    def test_duplicate_chunk_ids_removed(self):
        chunks = [
            {"chunk_id": 1, "text": "a", "similarity": 0.9},
            {"chunk_id": 1, "text": "a again", "similarity": 0.8},
            {"chunk_id": 2, "text": "b", "similarity": 0.5},
        ]
        result = rerank_chunks(chunks)
        assert len(result) == 2

    def test_sorted_by_similarity_descending(self):
        chunks = [
            {"chunk_id": 1, "text": "low", "similarity": 0.2},
            {"chunk_id": 2, "text": "high", "similarity": 0.9},
        ]
        result = rerank_chunks(chunks)
        assert result[0]["text"] == "high"
