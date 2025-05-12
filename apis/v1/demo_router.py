from fastapi import APIRouter, Depends, HTTPException, status
from apis.models.ask import AskModel
from core.clients.groq import GroqClient as client
from core.logics.demo import generate_answer_with_index

router = APIRouter(
    prefix="/demo",
    tags=["ask questions basing on agri_chatbot and vns_policy indices"]
)

# Dependency Injection
def get_client() -> object:
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM client not available"
        )
    return client

@router.post("/agriculture", summary="Generate answer with specified Meilisearch index: agri_chatbot")
def get_answer_by_index(
    request: AskModel,
    client: object = Depends(get_client)
):
    return generate_answer_with_index("agri_chatbot", request, client)

@router.post("/vns_policy", summary="Generate answer with specified Meilisearch index: vns_policy")
def get_answer_by_index(
    request: AskModel,
    client: object = Depends(get_client)
):
    return generate_answer_with_index("vns_policy", request, client)
