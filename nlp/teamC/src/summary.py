def summarize_text(text):
    if not text or len(text.strip()) == 0:
        return ""

    # Return first 100 characters as summary
    return text.strip()[:100]