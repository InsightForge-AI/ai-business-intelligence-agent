from sentiment.sentiment import analyze_sentiment

if __name__ == "__main__":
    text = input("Enter text: ")
    result = analyze_sentiment(text)

    print("Sentiment:", result["sentiment"])