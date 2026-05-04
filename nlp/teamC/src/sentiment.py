import re
from nlp.teamC.src.llm import ask_llm


def preprocess_text(text):
    
    if not text or not str(text).strip():
        return ""

    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)   # remove symbols
    text = re.sub(r"\s+", " ", text).strip()   # remove extra spaces
    return text


def get_sentiment(text):
    if not text or text.strip() == "":
        return "neutral"

    positive_words = {
      "good", "great", "excellent", "amazing", "nice", "worth", "fast", "love", "awesome", "fantastic", "perfect", "best", "wonderful", "superb",
      "brilliant", "outstanding", "cool", "happy", "satisfied", "pleasant", "impressive", "reliable", "smooth", "easy", "helpful", "beautiful",
      "strong", "smart", "recommend", "premium","valuable", "efficient", "quick", "positive", "enjoy", "liked", "favorite", "delightful","super",
      "fine","recommended","stylish","clear","stable","comfortable","nice"}

    negative_words = {
      "bad", "poor", "worst", "slow", "disappointing", "late", "hate","lately", "awful", "terrible", "horrible", "useless", "waste", "broken", "cheap","small", 
      "cheaper","weak", "boring", "annoying", "hard","difficult", "problem","problems", "issue","issues", "error","errors", "bug","bugs","buggy", "lag","lagged",
      "heating","delay","delayed","delays", "negative", "frustrating", "dirty", "ugly", "noisy","used","unclear","confusing","crash","crashes","crashed","expensive",
      "slow","overpriced", "damaged","damages", "unreliable", "fail","failed", "poorly", "dislike", "regret", "pathetic", "mess","stopped","messy","unstable",
      "heating","drains","limited","drained","low","heavy"}

    words = text.split()

    positive_count = sum(1 for word in words if word in positive_words)
    negative_count = sum(1 for word in words if word in negative_words)
   
    if "but" in words and positive_count > 0:
        return "mixed"
    elif positive_count > 0 and negative_count > 0:
    text = text.lower()

    positive_words = [
        "good","great","excellent","amazing","awesome","fast","smooth",
        "strong","reliable","easy","nice","beautiful","comfortable",
        "perfect","best","premium","stylish","impressive","love"
    ]

    negative_words = [
        "bad","poor","slow","late","worst","terrible","issue","problem",
        "error","bug","weak","damaged","crash","lag","difficult",
        "frustrating","disappointing","cheap","overheating"
    ]

    words = text.split()

    pos = sum(word in positive_words for word in words)
    neg = sum(word in negative_words for word in words)

    # mixed condition
    if pos > 0 and neg > 0:
        return "mixed"

    elif pos > neg:
        return "positive"

    elif neg > pos:
        return "negative"

    else:
        return "neutral"
    
#LLM Enhancement 

def smart_sentiment(text):

    basic_sentiment = get_sentiment(text)

    prompt = f"""
    You are a sentiment classifier.

    Text:
    \"\"\"{text}\"\"\"

    Initial prediction:
    {basic_sentiment}

   Check if the prediction is correct.

    Return ONLY one word from:
    positive, negative, neutral, mixed.
    No explanation.
    """

    llm_result = ask_llm(prompt)

    if llm_result:

        llm_result = llm_result.strip().lower()

        allowed = ["positive","negative","neutral","mixed"]

        if llm_result in allowed:

            # Trust rule-based if already confident
            if basic_sentiment in ["positive","negative","mixed"]:
                return basic_sentiment

            return llm_result

    return basic_sentiment
        return "neutral"
