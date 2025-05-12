from pydantic import BaseModel, Field
from typing import Optional, List

class AskModel(BaseModel):
    query: str = Field(..., description="User's current question or search query")
    history: Optional[List[str]] = Field(default_factory=list, description="Optional chat history to assist with context")
    
