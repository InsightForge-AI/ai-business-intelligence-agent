from typing import Any

from pydantic import BaseModel


class AnalyzeResponse(BaseModel):

    success: bool

    message: str

    data: Any