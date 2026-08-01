from typing import Any

from pydantic import BaseModel


class UploadResponse(BaseModel):

    success: bool

    message: str

    data: Any