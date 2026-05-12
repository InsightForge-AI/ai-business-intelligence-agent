from langchain_community.vectorstores import Chroma

def create_vectorstore(chunks, embeddings):

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="chroma_db"
    )

    return db