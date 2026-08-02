from pydantic import BaseModel
from typing import Optional, Dict, Any




class Document(BaseModel):


    file_id: str


    file_name: str


    file_type: str


    file_path: str



    file_size: Optional[int] = None



    # Saved AI Summary

    summary: Optional[Dict[str, Any]] = None



    # Future AI Insights

    insights: Optional[Dict[str, Any]] = None



    # Processing status

    status: Optional[str] = "Uploaded"


    ai_ready: bool = False