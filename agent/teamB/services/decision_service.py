def decide(query: str) -> str:
    if not query or not query.strip():
        return "unknown"

    q = query.lower()

    # Module → keywords mapping
    module_keywords = {
        "nlp": [
            "review", "reviews", "feedback", "comment", "comments",
            "sentiment", "summarize", "summary", "text", "language"
        ],
        "ml": [
            "sales", "revenue", "trend", "trends",
            "forecast", "forecasting", "prediction", "predict",
            "data", "metrics"
        ],
        "cv": [
            "image", "images", "video", "videos",
            "camera", "cctv", "detect", "footage", "detection", "object"
        ],
        "genai": [
            "generate", "create", "write", "explain",
            "report", "description"
        ]
    }

    # Priority order (highest → lowest)
    priority = ["nlp", "ml", "cv", "genai"]

    # Step 1: Find all matches
    matched_modules = []

    for module, keywords in module_keywords.items():
        if any(keyword in q for keyword in keywords):
            matched_modules.append(module)

    # Step 2: Apply priority
    for module in priority:
        if module in matched_modules:
            return module

    return "unknown"