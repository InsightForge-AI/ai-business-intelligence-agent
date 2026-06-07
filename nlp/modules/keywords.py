import re
from modules.llm_enhancer import ask_llm
from modules.prompts import keyword_prompt
import re



STOP_WORDS = {
    "the","this", "that","it","is","and","but","i","am","i'm", "a","an","to","of","or","was",
    "in","on","for","with","are","be","by","as","at","from","since","not","no","my","you","we","he",
    "she","they","have","has","had","do","does","did","will","would","could","should","may","might",
    "its","our","your","their","there","then","than","so","if","about","into","also","been","were","which",
    "what","when","how","who","can","just","me","him","her","us","them","any","all","more","very","too",
    "much","many","each","both","few","own","same","such","only","other","these","those","between",
    "through","after","before","over","under","again","further","once",
    # Extended — generic words that add no business meaning
    "due","up","two","three","four","five","while","stood","new","total",
    "currently","including","compared","following","using","across","enterprise",
    "enterprises","within","per","well","now","yet","still","already","however","although",
    "therefore","thus","hence","key","major","significant","strong","healthy",
    "successful","aggressive","primarily","significantly","ahead","steady",
    "zero","six","seven","eight","nine","ten","company","companies","business",
    "businesses","review","performance","initiative","initiatives","organization",
    "organizations","management","annual","year","years","period","report","reports"
}

# Chunk size in words for large text processing
CHUNK_SIZE = 200

# Max keywords cap
MAX_KEYWORDS = 20

# Short business terms to always allow (bypass len > 2 filter)
SHORT_WHITELIST = {"hr","ai","crm","erp","kpi","ceo","cfo","coo","roi","tax","rpa","nlp",
}



# Helpers

def _clean_text(text):
    
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _compute_target_length(word_count):
    
    
    if word_count <= 50:
        return 5
    elif word_count <= 150:
        return 8
    elif word_count <= 300:
        return 10
    elif word_count <= 600:
        return 13
    elif word_count <= 1000:
        return 16
    else:
        return MAX_KEYWORDS


def _chunk_words(words, chunk_size=CHUNK_SIZE):
    
    for i in range(0, len(words), chunk_size):
        yield words[i : i + chunk_size]



# Rule-based Layer

def get_keywords(text):
    
    if text is None:
        return ["No keywords found"]

    text = str(text)
    cleaned = _clean_text(text)

    if not cleaned:
        return ["No keywords found"]

    words = cleaned.split()

    #  Chunked extraction 
    keywords=[]
    seen = set()

    for chunk in _chunk_words(words, CHUNK_SIZE):

        for word in chunk:

            if (
                word not in STOP_WORDS
                and word not in seen
                and not word.isdigit()
                and (len(word) > 2 or word in SHORT_WHITELIST)
            ):
                keywords.append(word)
                seen.add(word)

    if not keywords:
        return ["No keywords found"]

# LLM Enhancement Layer



def smart_keywords(text):
    
    # Rule-based baseline 
    basic_keywords = get_keywords(text)

    if basic_keywords == ["No keywords found"]:
        return []

    basic_keyword_set = set(basic_keywords)


    # Determine target length 

    word_count = len(str(text).split())
    target = _compute_target_length(word_count)

    # ─ chunking strategy
    original_words = str(text).split()

    if word_count <= 500:
        text_chunks = [str(text)]
    else:
        text_chunks = [
            " ".join(chunk)
            for chunk in _chunk_words(original_words)
        ]

    merged_picks = []
    seen_picks = set()

   
    chunk_target = min(target + 5, MAX_KEYWORDS)

    for snippet in text_chunks:

        prompt = keyword_prompt(snippet,
                                basic_keywords,chunk_target)
        try:

            llm_result = ask_llm(prompt)

            if not llm_result:
                continue

            for word in llm_result.split(","):

                word = word.strip().lower()
                
                # Validate: must be in the rule-based list, no dupes

                if (
                    word in basic_keyword_set
                    and word not in seen_picks):

                    merged_picks.append(word)
                    seen_picks.add(word)

            # Early exit if we already have enough
            if len(merged_picks) >= target:
                break
        except Exception:
            continue


    # Trim to target & cap

    final_keywords = merged_picks[:target]

        # Fallback to rule-based keywords
    if not final_keywords:
        return basic_keywords[:target]
    
    return final_keywords
