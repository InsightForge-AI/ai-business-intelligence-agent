from typing import Any

from pydantic import BaseModel


class Metadata(BaseModel):

    document_type: str

    metadata: dict[str, Any]