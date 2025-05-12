from fastapi import APIRouter, Depends, HTTPException, status
import meilisearch
from apis.models.meilisearch import KeyWordSearchRequest, SemanticSearchRequest, HybridSearchRequest
from core.clients.meilisearch import MeiliClient as client
from core.logics.meilisearch import (
    handle_keyword_search,
    handle_semantic_search,
    handle_hybrid_search
)

router = APIRouter(prefix="/meilisearch", tags=["search references in Meilisearch db"])

def get_client() -> meilisearch.Client:
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Meilisearch client not available"
        )
    return client

@router.post("/keyword", summary="Perform keyword search using Meilisearch")
def keyword_search(
    request: KeyWordSearchRequest,
    client: meilisearch.Client = Depends(get_client)
):
    return handle_keyword_search(request, client)

@router.post("/semantic", summary="Perform semantic search with embedding")
def semantic_search(
    request: SemanticSearchRequest,
    client: meilisearch.Client = Depends(get_client)
):
    return handle_semantic_search(request, client)

@router.post("/hybrid", summary="Perform hybrid search with adjustable semantic ratio")
def hybrid_search(
    request: HybridSearchRequest,
    client: meilisearch.Client = Depends(get_client)
):
    return handle_hybrid_search(request, client)
