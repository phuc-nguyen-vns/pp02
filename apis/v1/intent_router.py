from fastapi import APIRouter, Depends, HTTPException, status
from apis.models.intent import IntentDetectionModel
from core.agents.prompts.content import IntentDetection
from openai import OpenAI
from config.contants import CATEGORIES_LIST
from core.clients.groq import GroqClient as client, model_name


# --- Initialize Router ---
router = APIRouter(prefix="/intent", tags=["intent-detection"])

# --- Dependency ---
def get_client() -> OpenAI:
    if client is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Meilisearch client not available")
    return client

# --- Intent Classification Endpoint ---
@router.post("/detect", summary="Classify intent using LLM and category list")
def classify_intent_with_history(
    request: IntentDetectionModel,
    client: OpenAI = Depends(get_client)
    ):
    content = IntentDetection.create_message_content(CATEGORIES_LIST, request.query, request.history)
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": content}
        ]
    )
    return completion.choices[0].message.content
