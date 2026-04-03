from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import re
from collections import Counter

app = FastAPI()

def extract_keywords(text: str, top_k: Optional[int] = None) -> List[str]:
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    
    stop_words = {'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have',
                  'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you',
                  'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'she'}
    
    words = [word for word in text.split() 
             if word not in stop_words and len(word) > 2]
    
    word_freq = Counter(words)
    
    if top_k is None:
        # Return ALL keywords (no limit)
        return [word for word, _ in word_freq.most_common()]
    else:
        # Return top K keywords
        return [word for word, _ in word_freq.most_common(top_k)]

class TextRequest(BaseModel):
    text: str
    top_k: Optional[int] = None  # Now optional - no default limit

@app.post("/extract-keywords")
def get_keywords(data: TextRequest):
    keywords = extract_keywords(data.text, data.top_k)
    return {
        "keywords": keywords,
        "count": len(keywords),
       
    }