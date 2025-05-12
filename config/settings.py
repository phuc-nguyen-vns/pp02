from pydantic_settings import BaseSettings
from pydantic import Field
from loguru import logger
from dotenv import load_dotenv
import os
import json
from typing import Optional, Dict, Any
from config.meilisearch_index_settings import MeiliIndexSettings

load_dotenv()


class Settings(BaseSettings):
    # General app info
    app_name: str = Field("Chatbot Backend", env="APP_NAME")
    debug_mode: bool = Field(False, env="DEBUG_MODE")

    # Meilisearch connection
    meilisearch_url: str = Field("http://192.168.1.174:7700/", env="MEILISEARCH_URL")
    meilisearch_token: str = Field(..., env="MEILISEARCH_TOKEN")

    # Meilisearch index settings (Typed!)
    meilisearch_index_settings: MeiliIndexSettings = MeiliIndexSettings()

    # Groq
    groq_url: Optional[str] = Field(None, env="GROQ_URL")
    groq_api_key: Optional[str] = Field(None, env="GROQ_API_KEY")
    groq_model_name: Optional[str] = Field(None, env="GROQ_MODEL_NAME")

    # openai
    openai_url: Optional[str] = Field(None, env="OPENAI_URL")
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    openai_model_name: Optional[str] = Field(None, env="OPENAI_MODEL_NAME")

    # Embedders
    embedder_1: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        env_file = ".env"
        case_sensitive = False

    def __init__(self, **values):
        super().__init__(**values)
        embedder_env = os.getenv("EMBEDDER_1")
        if embedder_env:
            try:
                self.embedder_1 = json.loads(embedder_env)
            except json.JSONDecodeError:
                logger.warning("Failed to parse EMBEDDER_1 as JSON. Using default {}.")


# Singleton instance for global import
settings = Settings()
