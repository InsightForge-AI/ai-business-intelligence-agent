import re
from collections import Counter

def extract_keywords(text):
    if not text or len(text.strip()) == 0:
        return []

    # Clean text
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)

    words = text.split()

    # Remove very short words (noise)
    words = [word for word in words if len(word) > 2]

    # Count frequency
    freq = Counter(words)

    # Get top 5 keywords
    keywords = [word for word, _ in freq.most_common(5)]

    return keywords