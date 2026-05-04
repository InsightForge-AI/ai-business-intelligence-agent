from nlp.teamC.src.llm import ask_llm

def get_keywords(text):

    # Preprocessing
    if text is None:
        return ["No keywords found"]

    text = str(text)

    # lowercase
    text = text.lower()

    # remove special characters
    import re
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    # Handle empty input
    if not text:
        return ["No keywords found"]

    words = text.split()

    stop_words = [
        "the","this","that","it", "is", "and", "but","i","am","i'm",
        "a", "an", "to", "of","or","was",
        "in", "on", "for", "with","are", "be", "by", "as", "at", "from","since"
          ]

    keywords = []
    seen = set()

    for word in words:

        if word not in stop_words:

            # Remove duplicates
            if word not in seen:
                keywords.append(word)
                seen.add(word)



    if len(keywords) == 0:
            return ["No keywords found"]

    return keywords

#LLM Enhancement

def smart_keywords(text):

    basic_keywords = get_keywords(text)

    prompt = f"""
    You are a keyword extraction assistant.

    Text:
    \"\"\"{text}\"\"\"

    Initial keywords:
    {basic_keywords}

    Rules:
    - Use ONLY keywords from the initial keywords list
    - Do NOT add new keywords
    - Remove only clearly duplicate or meaningless words
    - Keep meaningful descriptive words
    - Keep subject and feature words
    - Keep topic words and object names
    - Return keywords as a comma-separated list.
    - No sentences.No explanations
    """

    llm_result = ask_llm(prompt)

    if llm_result:

        words = llm_result.split(",")

        cleaned = [
            w.strip().lower()
            for w in words
        ]

        filtered = [
            w for w in cleaned
            if w in basic_keywords
        ]

        # Safety fallback
        if len(filtered) < 2:
            return basic_keywords

        return filtered

    return basic_keywords 