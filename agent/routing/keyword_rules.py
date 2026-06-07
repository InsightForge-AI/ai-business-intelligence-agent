"""
routing/keyword_rules.py
------------------------
The keyword dictionary that powers rule-based routing.

Each module maps to the trigger phrases that indicate the user wants that
kind of processing. Phrases are matched as substrings against the
normalized (lower-cased) question, so keep them lower-case here.

"""

KEYWORDS = {
    # --- Natural Language Processing -------------------------------------
    "nlp": [
        "summarize", "summarise", "summary", "overview", "tl;dr", "tldr",
        "sentiment", "tone", "emotion", "positive or negative",
        "classify", "classification", "categorize", "categorise",
        "translate", "translation",
        "key points", "keywords", "highlights",
        "paraphrase", "rewrite", "rephrase",
    ],

    # --- Machine Learning / structured analytics -------------------------
    "ml": [
        "sales", "revenue", "profit", "forecast", "predict", "prediction",
        "trend", "trends", "growth", "decline", "drop",
        "kpi", "kpis", "metric", "metrics", "analytics", "statistics",
        "region", "regions", "quarter", "monthly", "yearly",
        "correlation", "regression", "cluster", "segment", "segmentation",
        "anomaly", "outlier", "low sales", "high sales",
        "best performing", "worst performing", "performance",
    ],

    # --- Computer Vision -------------------------------------------------
    "cv": [
        "image", "picture", "photo", "ocr", "scan", "scanned",
        "detect", "detection", "object", "objects",
        "what is in", "what's in", "what is shown", "visible in",
        "logo", "face", "read the text from",
    ],

    # --- Retrieval-Augmented Generation / document QA --------------------
    "rag": [
        "answer", "question", "q&a",
        "according to", "from this document", "from the document",
        "from this pdf", "from the pdf", "find in the",
        "retrieve", "look up", "based on the document",
    ],
}
