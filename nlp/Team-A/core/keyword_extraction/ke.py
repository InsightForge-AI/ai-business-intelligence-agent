import re
from collections import Counter
from typing import List, Optional

from app.models.ke_bm import get_stopwords

stop_words = get_stopwords()


def extract_keywords(text: str, top_k: Optional[int] = None) -> List[str]:
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)

    words = [
        word for word in text.split()
        if word not in stop_words and len(word) > 2
    ]

    word_freq = Counter(words)

    if top_k is None:
        return [word for word, _ in word_freq.most_common()]
    else:
        return [word for word, _ in word_freq.most_common(top_k)]