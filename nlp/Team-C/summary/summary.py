import heapq
import re
from collections import defaultdict

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


stop_words = set(stopwords.words("english"))


def summarize_text(text, num_sentences=2):
    if not text or len(text.strip()) == 0:
        return ""

 
    text = re.sub(r'\s+', ' ', text)

    
    sentences = sent_tokenize(text)

    
    if len(sentences) <= num_sentences:
        return text

    
    word_freq = defaultdict(int)

    for word in word_tokenize(text.lower()):
        if word.isalnum() and word not in stop_words:
            word_freq[word] += 1

    if not word_freq:
        return text

    
    max_freq = max(word_freq.values())
    for word in word_freq:
        word_freq[word] /= max_freq

    
    sentence_scores = defaultdict(int)

    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in word_freq:
                sentence_scores[sent] += word_freq[word]

    
    summary_sentences = heapq.nlargest(
        num_sentences, sentence_scores, key=sentence_scores.get
    )

    return " ".join(summary_sentences)