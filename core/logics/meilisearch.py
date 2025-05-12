from fastapi import HTTPException
from core.embedders import embedder_1
import meilisearch
from apis.models.meilisearch import KeyWordSearchRequest, SemanticSearchRequest, HybridSearchRequest

def handle_keyword_search(request: KeyWordSearchRequest, client: meilisearch.Client):
    return client.index(request.index).search(
        request.query,
        {'limit': request.top_k}
    )

def handle_semantic_search(request: SemanticSearchRequest, client: meilisearch.Client):
    if request.embedder == 'embedder':
        query_vector = embedder_1.embedding(request.query)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Embedder '{request.embedder}' is not defined. Available: ['embedder_1']"
        )
    return client.index(request.index).search(
        request.query,
        {
            'vector': query_vector,
            'hybrid': {
                "embedder": request.embedder,
                "semanticRatio": 1.0
            },
            'limit': request.top_k
        }
    )

def handle_hybrid_search(request: HybridSearchRequest, client: meilisearch.Client):
    if request.embedder == 'embedder':
        query_vector = embedder_1.embedding(request.query)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Embedder '{request.embedder}' is not defined. Available: ['embedder_1']"
        )
    return client.index(request.index).search(
        request.query,
        {
            'vector': query_vector,
            'hybrid': {
                "embedder": request.embedder,
                "semanticRatio": request.semantic_ratio
            },
            'limit': request.top_k
        }
    )
