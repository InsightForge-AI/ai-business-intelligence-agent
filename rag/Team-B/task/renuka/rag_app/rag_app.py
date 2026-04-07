import os

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import HuggingFacePipeline

from transformers import pipeline

# -------------------------------
# STEP 1: LOAD DATA
# -------------------------------
loader = TextLoader("data/knowledge.txt")
documents = loader.load()

# -------------------------------
# STEP 2: CHUNKING
# -------------------------------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

# -------------------------------
# STEP 3: EMBEDDINGS (FREE)
# -------------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -------------------------------
# STEP 4: VECTOR DATABASE
# -------------------------------
vector_db = FAISS.from_documents(chunks, embeddings)

# -------------------------------
# STEP 5: RETRIEVER
# -------------------------------
retriever = vector_db.as_retriever()

# -------------------------------
# STEP 6: LOCAL LLM (IMPROVED)
# -------------------------------
pipe = pipeline(
    "text-generation",
    model="gpt2",   # 🔥 UPDATED MODEL (better than distilgpt2)
    max_new_tokens=80
)

llm = HuggingFacePipeline(pipeline=pipe)

# -------------------------------
# STEP 7: QUERY LOOP
# -------------------------------
print("\nRAG App Ready! Type 'exit' to quit\n")

while True:
    query = input("You: ")

    if query.lower() in ["exit", "quit"]:
        print("Exiting RAG App... 👋")
        break

    # Retrieve documents
    docs = retriever.invoke(query)

    # Combine context
    context = "\n".join([doc.page_content for doc in docs])

    # 🔥 IMPROVED PROMPT
    prompt = ChatPromptTemplate.from_template(
        "You are a helpful assistant.\n"
        "Answer clearly in 1-2 sentences.\n"
        "Do not repeat the question.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answer:"
    )

    # Chain
    chain = prompt | llm

    # Get response
    result = chain.invoke({
        "context": context,
        "question": query
    })

    # Clean output
    print("AI:", str(result).split("Answer:")[-1].strip())