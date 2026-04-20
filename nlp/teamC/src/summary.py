import re

def summarize_text(text):
    if not text or text.strip() == "":
        return "Empty."

    # remove special characters
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)

    # remove extra spaces
    clean_text = " ".join(clean_text.split())

    # Capitalize first letter (optional)
    clean_text = clean_text.strip()

    # ensure ending with "."
    if not clean_text.endswith("."):
        clean_text += "."

    return clean_text