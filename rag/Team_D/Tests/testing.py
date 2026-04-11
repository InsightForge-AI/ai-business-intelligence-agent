# This module is done by Mahesh

import requests

BASE_URL = "http://127.0.0.1:8000"


def test_query(query):
    try:
        response = requests.post(
            f"{BASE_URL}/rag/query",
            json={"query": query}
        )

        print(f"\n🔍 Query: {query}")
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("\nAnswers:")
            for i, ans in enumerate(data.get("answers", []), 1):
                print(f"{i}. {ans}")
        else:
            print("Error:", response.text)

    except Exception as e:
        print("🚨 Request failed:", e)


if __name__ == "__main__":
    print("🧪 API Testing Started (type 'exit' to stop)\n")

    while True:
        q = input("Enter query: ")

        if q.lower() == "exit":
            break

        test_query(q)