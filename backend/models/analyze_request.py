from pydantic import BaseModel


class AnalyzeRequest(BaseModel):

    file_id: str

    query: str