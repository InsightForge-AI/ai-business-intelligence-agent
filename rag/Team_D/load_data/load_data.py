# Read file
def load_faq_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().lower()

# Process text
    parts = text.split("question")

    docs = []
    for part in parts:
        if "answer" in part:
            # split question and answer
            qa = part.split("answer")

            if len(qa) > 1:
                answer = qa[1].strip()   #  ONLY ANSWER
                docs.append(answer)
    return docs
