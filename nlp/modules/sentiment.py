import re
from modules.llm_enhancer import ask_llm
from modules.prompts import sentiment_prompt

POSITIVE_WORDS = {
    # General Positive
    "good", "great", "excellent", "amazing", "nice", "worth",
    "fast", "love", "awesome", "fantastic", "perfect", "best",
    "wonderful", "superb", "brilliant", "outstanding", "cool",
    "happy", "satisfied", "pleasant", "impressive", "reliable",
    "smooth", "easy", "helpful", "beautiful", "strong", "smart",
    "recommend", "recommended", "premium", "valuable", "efficient",
    "quick", "positive", "enjoy", "liked", "favorite", "delightful",
    "super", "fine", "stylish","clear", "stable", "comfortable",

    # Business Positive
    "growth", "growing","profit", "profits", "profitable","revenue", "revenues",
    "gain", "gains", "increase", "increased", "improvement", "improved",
    "success", "successful","opportunity", "opportunities","expansion", "expanded",
    "innovation", "innovative","productive", "productivity","achievement", "achievements",
    "competitive", "leader", "leadership","performance", "performing","boost", "boosted"
}


NEGATIVE_WORDS = {
    # General Negative
    "bad", "poor", "worst", "slow", "disappointing", "late",
    "hate", "awful", "terrible", "horrible", "useless",
    "waste", "broken", "weak", "boring", "annoying",
    "hard", "difficult", "problem", "problems", "issue",
    "issues", "error", "errors", "bug", "bugs", "buggy",
    "lag", "lagged", "heating", "delay", "delayed",
    "delays", "negative", "frustrating", "dirty", "ugly",
    "noisy", "unclear", "confusing", "crash", "crashes",
    "crashed", "expensive", "overpriced", "damaged",
    "damages", "unreliable", "fail", "failed", "poorly",
    "dislike", "regret", "pathetic", "mess", "stopped",
    "messy", "unstable", "drains", "limited", "drained",

    # Business Negative
    "loss", "losses","decline", "declined","decrease", "decreased",
    "drop", "dropped","risk", "risks","debt", "debts","failure", "failing",
    "bankruptcy", "bankrupt","challenge", "challenges","threat", "threats",
    "downturn", "shortage","inflation", "recession","weakness",
    "penalty", "penalties","lawsuit", "lawsuits"
}


NEGATION_WORDS = {"not", "never", "no"}


def preprocess_text(text):
    

    if not text or not str(text).strip():
        return ""

    text = str(text).lower()

    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def get_sentiment(text):
    

    text = preprocess_text(text)

    if not text:
        return "neutral"

    words = text.split()

    positive_count = 0
    negative_count = 0

    skip_next = False

    for i, word in enumerate(words):

        if skip_next:
            skip_next = False
            continue

        # Handle negations
        if (
            word in NEGATION_WORDS
            and i + 1 < len(words)
        ):

            next_word = words[i + 1]

            if next_word in POSITIVE_WORDS:
                negative_count += 1
                skip_next = True
                continue

            elif next_word in NEGATIVE_WORDS:
                positive_count += 1
                skip_next = True
                continue

        # Normal counting
        if word in POSITIVE_WORDS:
            positive_count += 1

        elif word in NEGATIVE_WORDS:
            negative_count += 1

    # Final sentiment
    if positive_count > 0 and negative_count > 0:
        return "mixed"

    elif positive_count > negative_count:
        return "positive"

    elif negative_count > positive_count:
        return "negative"

    return "neutral"


def smart_sentiment(text):
    """
    LLM-enhanced sentiment analysis.

    Flow:
    1. Run rule-based sentiment.
    2. Send text + rule-based prediction to LLM.
    3. If LLM returns valid label -> use it.
    4. Else return rule-based result.
    """

    basic_sentiment = get_sentiment(text)

    prompt = sentiment_prompt(text, basic_sentiment)

    try:

        llm_result = ask_llm(prompt)

        if llm_result:

            llm_result = llm_result.strip().lower()

            allowed = {
                "positive",
                "negative",
                "neutral",
                "mixed"
            }

            if llm_result in allowed:
                return llm_result

    except Exception:
        pass

    return basic_sentiment