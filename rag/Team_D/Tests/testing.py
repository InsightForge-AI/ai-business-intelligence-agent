# This module is done by Mahesh

import requests

BASE_URL = "http://127.0.0.1:8000"


def test_query(query):
    response = requests.post(
        f"{BASE_URL}/rag/query",
        json={"query": query}
    )

    print(f"\nQuery: {query}")
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print("Answers:")
        for i, ans in enumerate(data.get("answers", []), 1):
            print(f"{i}. {ans}")
    else:
        print("Error:", response.text)


if __name__ == "__main__":
    while True:
        q = input("Enter query (or 'exit'): ")
        if q.lower() == "exit":
            break
        test_query(q)