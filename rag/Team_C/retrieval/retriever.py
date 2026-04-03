
guru vishnu kavuturu
2:06 PM
git checkout -b teamC/ranking-module

guru vishnu kavuturu
2:29 PM
def rank_results(results):

    ranked = sorted(results, key=lambda x: x["score"], reverse=True)

    return ranked

guru vishnu kavuturu
2:35 PM
git commit -m "feat: ranking engine for retrieval results"

guru vishnu kavuturu
2:40 PM
git checkout dev
git pull origin dev

git checkout -b teamC/response-module

guru vishnu kavuturu
2:41 PM
git checkout dev
git pull origin dev

git checkout -b teamC/retrieval-module
git add rag/teamC/retrieval/
git commit -m "feat: document retrieval module"
git push origin teamC/retrieval-module

guru vishnu kavuturu
2:45 PM
from rag.teamC.vector_store.store import load_documents


def retrieve_documents(tokens):

    docs = load_documents()

    results = []

    for doc in docs:

        score = 0

        for token in tokens:

            if token in doc["text"]:
                score += 1

        if score > 0:

            results.append({
                "id": doc["id"],
                "text": doc["text"],
                "score": score
            })

    return results