import os
import importlib.util


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SRC = os.path.dirname(__file__)

preprocess   = load("preprocess", os.path.join(SRC, "preprocess.py")).preprocess
get_insights = load("insights",     os.path.join(SRC, "insights.py")).get_insights


def analyze(query: str, call_llm) -> dict:
    # Step 1 — clean and validate query
    clean_query = preprocess(query)
    if not clean_query:
        return {"total_sales": None, "top_product": None, "trend": None, "error": "Empty or invalid query", "insights": None}

    # Step 2 — get insights from LLM
    return get_insights(clean_query, call_llm)