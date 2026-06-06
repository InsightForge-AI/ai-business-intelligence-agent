from modules.llm_enhancer import ask_llm
from modules.prompts import summary_prompt
import re


def preprocess(text):

    if not text or not str(text).strip():
        return None

    cleaned = text.lower()

    cleaned = re.sub(
        r'[^a-z0-9\s\.]',
        ' ',
        cleaned
    )

    cleaned = " ".join(cleaned.split())

    return cleaned


def summarize(text):

   # Core extractive summarizer


    if not text or not str(text).strip():
        return "No text provided"

    clean_original = re.sub(
        r'[^a-zA-Z0-9\s\.]',
        ' ',
        text
    )

    clean_original = " ".join(clean_original.split())

    original_sentences = re.split(
        r'\.+\s*',
        clean_original
    )

    original_sentences = [
        s.strip()
        for s in original_sentences
        if s.strip()
    ]

    cleaned_text = preprocess(text)

    if not cleaned_text:
        return "No text provided"

    cleaned_sentences = re.split(
        r'\.+\s*',
        cleaned_text
    )

    cleaned_sentences = [
        s.strip()
        for s in cleaned_sentences
        if s.strip()
    ]

    total_sentences = len(original_sentences)

    if total_sentences <= 1:
        return (
            original_sentences[0] + "."
            if original_sentences
            else "No text provided"
        )

    summary_length = max(
        3,
        min(
            round(total_sentences * 0.30),
            40
        )
    )

    stop_words = {
        "the", "is", "and", "but",
        "a", "an", "to", "of",
        "in", "on", "for", "with",
        "at", "by", "this", "that",
        "these", "those", "it",
        "its", "was", "were",
        "are", "be", "been",
        "being", "as", "from",
        "or", "if", "into",
        "about", "over", "under",
        "between", "during",
        "however", "overall"
    }

    word_freq = {}

    for sentence in cleaned_sentences:

        for word in sentence.split():

            if word not in stop_words:

                word_freq[word] = (
                    word_freq.get(word, 0) + 1
                )

    sentence_scores = {}

    for i, sentence in enumerate(cleaned_sentences):

        words = sentence.split()

        if not words:
            continue

        score = sum(
            word_freq.get(word, 0)
            for word in words
        )

        score = score / len(words)

        if i == 0:
            score += 2

        sentence_scores[i] = score

    top_indexes = sorted(
        sentence_scores,
        key=sentence_scores.get,
        reverse=True
    )[:summary_length]

    top_indexes = sorted(top_indexes)

    selected_sentences = [
        original_sentences[i]
        for i in top_indexes
        if i < len(original_sentences)
    ]

    selected_sentences = list(
        dict.fromkeys(selected_sentences)
    )

    return ". ".join(selected_sentences) + "."


def get_summary(text):
    
    # Handles small and large documents
    

    if not text or not str(text).strip():
        return "No text provided"

    sentences = re.split(
        r'\.+\s*',
        text
    )

    sentences = [
        s.strip()
        for s in sentences
        if s.strip()
    ]

    # Small document
    if len(sentences) <= 100:
        return summarize(text)

    # Large document
    chunk_size = 100

    chunks = []

    for i in range(
        0,
        len(sentences),
        chunk_size
    ):

        chunk = ". ".join(
            sentences[i:i + chunk_size]
        )

        chunks.append(chunk)

    chunk_summaries = []

    for chunk in chunks:

        chunk_summaries.append(
            summarize(chunk)
        )

    combined_summary = ". ".join(
        chunk_summaries
    )

    return summarize(combined_summary)


def smart_summary(text):

    base_summary = get_summary(text)
    
    if base_summary == "No text provided":
        return "No text provided"

    prompt = summary_prompt(base_summary)
 
    try:

        llm_result = ask_llm(prompt)

        if (
            llm_result
            and isinstance(llm_result, str)
            and llm_result.strip()
        ):
            return llm_result.strip()

    except Exception:
        pass

    return base_summary