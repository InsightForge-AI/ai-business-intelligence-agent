# This module is done by Mahesh

import subprocess
import time
import requests
import sys

BASE_URL = "http://127.0.0.1:8000"


def start_server():
    print("🚀 Starting FastAPI server...")

    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "rag.Team_D.main:app", "--reload"]
    )

    time.sleep(6)  # wait for server to start
    return process


def test_query(query):
    try:
        response = requests.post(
            f"{BASE_URL}/ask",
            json={"query": query}
        )

        print(f"\n🔍 Query: {query}")
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("Answers:")
            for i, ans in enumerate(data.get("answers", []), 1):
                print(f"{i}. {ans}")
        else:
            print("Error:", response.text)

    except Exception as e:
        print("🚨 Request failed:", e)


if __name__ == "__main__":
    server = start_server()

    try:
        print("\n🧪 Testing API (type 'exit' to stop)\n")

        while True:
            q = input("Enter query: ")

            if q.lower() == "exit":
                break

            test_query(q)

    finally:
        print("\n🛑 Stopping server...")
        server.terminate()
# Testing module placeholder

if __name__ == "__main__":
    print("Testing module initialized")
