def search(query, data):
    query_words=query.lower().split()
    results=[]

    for item in data:
        doc_words=item["content"].lower().split()
        score=len(set(query_words) & set(doc_words))

        if score>0:
            results.append((score,item))

    results.sort(reverse=True,key=lambda x: x[0])
    
    return [doc for _,doc in results[:3]]