from langchain_core.documents import Document
from app.data.hospital_data import hospital_data

def load_documents():

    documents = []

    for item in hospital_data:

        content = f'''
        Question:
        {item["question"]}

        Answer:
        {item["answer"]}
        '''

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": "hospital_data"
                }
            )
        )

    return documents