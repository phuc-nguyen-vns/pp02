from pydantic import BaseModel, Field
from typing import Optional, List

class IntentDetectionModel(BaseModel):
    query: str = Field(..., description="User search query")
    history: Optional[List[str]] = Field(default_factory=list, description="Optional chat history to assist with context")

    class Config:
        extra = "allow"  # Allow additional arbitrary key-value params



