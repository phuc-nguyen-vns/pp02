from pydantic import BaseModel, Field
from typing import Optional, Dict, List


class TypoTolerance(BaseModel):
    enabled: bool = True
    minWordSizeForTypos: Dict[str, int] = Field(default_factory=lambda: {"oneTypo": 5, "twoTypos": 9})


class EmbedderSettings(BaseModel):
    source: str = "userProvided"
    dimensions: int = 1024


class MeiliIndexSettings(BaseModel):
    dictionary: List[str] = Field(default_factory=list)
    stopWords: List[str] = Field(default_factory=list)
    typoTolerance: TypoTolerance = TypoTolerance()
    synonyms: Dict[str, str] = Field(default_factory=dict)
    separatorTokens: List[str] = Field(default_factory=list)
    nonSeparatorTokens: List[str] = Field(default_factory=list)
    
    displayedAttributes: Optional[List[str]] = None  # Example: ['*']
    searchableAttributes: List[str] = Field(default_factory=lambda: ["content"])
    filterableAttributes: List[str] = Field(default_factory=lambda: ["filename", "page", "chunk"])
    sortableAttributes: List[str] = Field(default_factory=lambda: ["page", "chunk"])
    distinctAttribute: Optional[str] = None
    rankingRules: Optional[List[str]] = None
    embedders: Dict[str, EmbedderSettings] = Field(default_factory=lambda: {
        "embedder": EmbedderSettings()
    })
