# This module is done by Mahesh

import requests

BASE_URL = "http://127.0.0.1:8000"


def test_query(query, test_case_name=""):
    try:
        response = requests.post(
            f"{BASE_URL}/rag/query",
            json={"query": query}
        )

        print(f"\n🔍 Test Case: {test_case_name}")
        print(f"Query: {query}")
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("\nResponse:")
            for key, value in data.items():
                print(f"  {key}: {value}")
        else:
            print("Error:", response.text)

    except Exception as e:
        print("🚨 Request failed:", e)


def run_edge_case_tests():
    """
    Test all 8 edge cases for RAG module
    """
    edge_cases = [
        ("sales dropped", "Normal Query"),
        ("", "Empty Query"),
        ("weather today", "No Match"),
        ("SALES DROPPED", "Case Sensitivity"),
        ("sales  dropped", "Extra Spaces"),
        ("sales decrease reason", "Partial Match"),
        ("sales sales sales", "Duplicate Words"),
        ("long paragraph asking business sales reasons", "Long Query"),
    ]
    
    print("=" * 60)
    print("🧪 RAG Module - Edge Case Testing")
    print("=" * 60)
    
    for query, case_name in edge_cases:
        test_query(query, case_name)
        print("-" * 60)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "edge":
        # Run automated edge case tests
        run_edge_case_tests()
    else:
        # Interactive mode
        print("🧪 API Testing Started (type 'exit' to stop)\n")
        print("Tips:")
        print("  - Run 'python testing.py edge' to run all edge case tests")
        print("  - Or enter queries interactively below\n")

        while True:
            q = input("Enter query: ")

            if q.lower() == "exit":
                break

            test_query(q)