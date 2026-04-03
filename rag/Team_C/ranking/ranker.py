def rank_results(results):

    ranked = sorted(results, key=lambda x: x["score"], reverse=True)

    return ranked