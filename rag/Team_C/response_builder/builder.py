def build_response(query, ranked_results, top_k=3):

    top_results = ranked_results[:top_k]

    response = {
        "query": query,
        "top_k": top_k,
        "results": top_results
    }

    return response
