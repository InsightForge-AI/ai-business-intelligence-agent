import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import defaultdict
from preprocessing import clean_text  

nltk.download('punkt')
nltk.download('punkt_tab')

def summarize_text(text, num_sentences=2):
    
    sentences = sent_tokenize(text)

    if len(sentences) <= num_sentences:
        return text

  
    cleaned_text = clean_text(text)

    
    words = word_tokenize(cleaned_text)

    
    word_frequencies = defaultdict(int)
    for word in words:
        word_frequencies[word] += 1

    
    sentence_scores = defaultdict(int)

    for sentence in sentences:
        clean_sentence = clean_text(sentence)
        for word in word_tokenize(clean_sentence):
            if word in word_frequencies:
                sentence_scores[sentence] += word_frequencies[word]

    
    sorted_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)


    summary = " ".join(sorted_sentences[:num_sentences])

    return summary