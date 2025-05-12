from fastapi import APIRouter, Depends, HTTPException, status

from apis.models.chat import ChatGenerationModel
from core.clients.groq import GroqClient as client
from core.logics.chat import generate_answer, generate_next_question

# Initialize Router
router = APIRouter(prefix="/chat", tags=["chat-generation"])

# Dependency Injection
def get_client() -> object:
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM client not available"
        )
    return client

@router.post("/answer_question", summary="Generate answer using LLM and Meilisearch context")
def get_answer(
    request: ChatGenerationModel,
    client: object = Depends(get_client)
):
    return generate_answer(request, client)

@router.post("/next_question", summary="Generate next question using LLM and Meilisearch context")
def next_question(
    request: ChatGenerationModel,
    client: object = Depends(get_client)
):
    return generate_next_question(request, client)
