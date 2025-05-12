from pydantic import BaseModel, Field
from typing import Optional, List

class ChatGenerationModel(BaseModel):
    query: str = Field(..., description="User's current question or search query")
    search_type: Optional[str] = Field(default="keyword_search", description="Search method: keyword_search, semantic_search, or hybrid_search")
    semantic_ratio: Optional[float] = Field(default=0.5, description="Semantic weight for hybrid search (0 to 1)")
    embedder: Optional[str] = Field(default="embedder", description="Embedding model name")
    top_k: Optional[int] = Field(default=3, description="Number of results to retrieve from search")
    index: Optional[str] = Field(default="vns_policy", description="Target index to search")
    history: Optional[List[str]] = Field(default_factory=list, description="Optional list of previous user messages")
