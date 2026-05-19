def retrieve_context(db, query):

    retriever = db.as_retriever(
        search_kwargs={"k": 3}
    )

    docs = retriever.invoke(query)

    return docs
