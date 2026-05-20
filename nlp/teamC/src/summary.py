import re

from nlp.teamC.src.preprocessing import clean_text
from nlp.teamC.src.llm import ask_llm


stop_words = {
    "the", "is", "and", "a", "an",
    "to", "of", "in", "on", "for",
    "with", "this", "that", "it"
}


def summarize(text):

    try:

        if not text:
            return "No text provided"

        original_sentences = re.split(r"[.!?]+", text)

        original_sentences = [
            s.strip()
            for s in original_sentences
            if s.strip()
        ]

        cleaned = clean_text(text)

        cleaned_sentences = re.split(r"[.!?]+", cleaned)

        cleaned_sentences = [
            s.strip()
            for s in cleaned_sentences
            if s.strip()
        ]

        if len(original_sentences) == 1:
            return original_sentences[0]

        word_freq = {}

        for sentence in cleaned_sentences:

            words = sentence.split()

            for word in words:

                if word not in stop_words:

                    word_freq[word] = (
                        word_freq.get(word, 0) + 1
                    )

        sentence_scores = {}

        for i, sentence in enumerate(cleaned_sentences):

            words = sentence.split()

            if not words:
                continue

            score = 0

            for word in words:

                if word in word_freq:
                    score += word_freq[word]

            # normalize score
            score = score / len(words)

            # slight importance to first sentence
            if i == 0:
                score += 1

            sentence_scores[i] = score

        ranked = sorted(
            sentence_scores,
            key=sentence_scores.get,
            reverse=True
        )

        top_n = min(3, len(ranked))

        selected_indexes = sorted(ranked[:top_n])

        selected_sentences = [
            original_sentences[i]
            for i in selected_indexes
        ]

        return ". ".join(selected_sentences) + "."

    except Exception:
        return "Summary generation failed"


def smart_summary(text):

    try:

        base_summary = summarize(text)

        prompt = f"""
You are a text summarization assistant.

Text:
\"\"\"{text}\"\"\"

Initial summary:
{base_summary}

Rules:
- Improve readability
- Keep concise
- No explanation
"""

        llm_result = ask_llm(prompt)

        if llm_result:
            return llm_result.strip()

        return base_summary

    except Exception:
        return summarize(text)