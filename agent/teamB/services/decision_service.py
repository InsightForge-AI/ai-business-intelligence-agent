import re
from collections import defaultdict
from services.llm_service import ask_llm
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

# Patterns
NON_ALNUM_PATTERN = re.compile(r"[^a-z0-9\s]+")
SPACE_PATTERN = re.compile(r"\s+")


def normalize_query(query: str | None) -> str:
    text = "" if query is None else str(query)
    text = text.lower().strip()
    text = NON_ALNUM_PATTERN.sub(" ", text)
    return SPACE_PATTERN.sub(" ", text).strip()


def tokenize(text: str) -> list:
    return text.split()


def decide(query: str) -> dict:
    try:
        # Normalize
        normalized_query = normalize_query(query)

        if not normalized_query:
            return {
                "modules": ["nlp"],
                "confidence": 0.0
            }

        # Tokenize
        tokens = tokenize(normalized_query)

        # Stem tokens
        stemmed_tokens = [stemmer.stem(t) for t in tokens]

        # Weighted keywords
        module_keywords = {
            "nlp": {
                "review": 2,
                "feedback": 2,
                "comment": 1,
                "sentiment": 3,
                "summarize": 3,
                "summary": 2,
                "text": 0.5,
                "language": 0.5
            },
            "ml": {
                "sales": 2,
                "revenue": 2,
                "trend": 2,
                "forecast": 3,
                "predict": 3,
                "data": 0.5,
                "metrics": 1
            },
            "cv": {
                "image": 2,
                "video": 2,
                "camera": 1,
                "cctv": 2,
                "detect": 3,
                "object": 2,
                "footage": 2
            },
            "genai": {
                "generate": 3,
                "create": 2,
                "write": 2,
                "explain": 2,
                "report": 1,
                "description": 1
            }
        }

        # Phrase boosts
        module_phrases = {
            "nlp": {
                "customer review": 5,
                "user feedback": 5
            },
            "ml": {
                "sales trend": 5,
                "revenue forecast": 5
            },
            "cv": {
                "object detection": 5,
                "video footage": 4
            },
            "genai": {
                "generate report": 5,
                "create summary": 5
            }
        }

        scores = defaultdict(float)

        # Token scoring
        for module, keywords in module_keywords.items():
            for keyword, weight in keywords.items():
                if stemmer.stem(keyword) in stemmed_tokens:
                    scores[module] += weight

        # Phrase scoring
        for module, phrases in module_phrases.items():
            for phrase, weight in phrases.items():
                phrase_words = phrase.split()
                stemmed_phrase = [stemmer.stem(w) for w in phrase_words]
                length = len(stemmed_phrase)

                for i in range(len(stemmed_tokens) - length + 1):
                    if stemmed_tokens[i:i + length] == stemmed_phrase:
                        scores[module] += weight

        # Fallback
        if not any(score > 0 for score in scores.values()):
            return {
                "modules": ["nlp"],
                "confidence": 0.0
            }

        # Multi-intent filtering
        max_score = max(scores.values())
        threshold = max_score * 0.6

        filtered = {
            m: s for m, s in scores.items()
            if s >= threshold
        }

        # Sort modules
        sorted_modules = sorted(
            filtered.items(),
            key=lambda x: -x[1]
        )

        modules = [m for m, _ in sorted_modules]

        # Confidence
        sorted_scores = sorted(scores.values(), reverse=True)

        if len(sorted_scores) > 1:
            confidence = round(
                (sorted_scores[0] - sorted_scores[1]) / sorted_scores[0],
                2
            )
        else:
            confidence = 1.0

        # LLM validation/reranking
        validated_modules = ask_llm(query, modules)

        return {
            "modules": validated_modules,
            "confidence": confidence
        }

    except Exception:
        return {
            "modules": ["nlp"],
            "confidence": 0.0
        }