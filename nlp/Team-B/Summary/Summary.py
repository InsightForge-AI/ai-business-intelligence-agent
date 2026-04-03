def get_summary(text):

    sentences = text.split(".")

    summary = sentences[0]

    return summary.strip()


# TEST BLOCK
if __name__ == "__main__":

    text = "This product is good. It works very well."

    result = get_summary(text)

    print(result)