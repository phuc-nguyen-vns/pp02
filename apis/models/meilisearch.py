from pydantic import BaseModel, Field
from typing import Optional

# --- Base class with shared search fields ---
class SearchParamsModel(BaseModel):
    query: str = Field(..., description="User search query")
    top_k: Optional[int] = Field(default=3, description="Maximum number of search results to return")
    index: Optional[str] = Field(default="vns_policy", description="Meilisearch index to search")

    class Config:
        extra = "allow"  # Allow additional arbitrary key-value params



# === Search Models ===

class KeyWordSearchRequest(SearchParamsModel):
    pass  # Uses only the base fields

class SemanticSearchRequest(SearchParamsModel):
    embedder: Optional[str] = Field(default="embedder", description="Embedder model name")

class HybridSearchRequest(SemanticSearchRequest):
    embedder: Optional[str] = Field(default="embedder", description="Embedder model name")
    semantic_ratio: float = Field(default=0.5, description="Ratio between semantic and keyword scores (0–1)")

