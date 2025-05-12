from fastapi import APIRouter, Depends, HTTPException, status
import sys, os, json
from pathlib import Path

# --- Add Project Path ---
sys.path.append(Path(os.getcwd(), "PP02").as_posix())

# --- Import Internal Modules ---
from apis.models.ask import AskModel
from core.clients.groq import GroqClient as client, model_name
from core.clients.meilisearch import MeiliClient as meili_client
from core.agents.prompts.content import  AgricultureAnswerGeneration, DemoAnswerGeneration    
from core.embedders import embedder_1

# --- Initialize Router ---
router = APIRouter(
    prefix="/chat",
    tags=["ask questions about vns_policy or agriculture"]
)

# --- Dependency Injection ---
def get_client() -> object:
    if meili_client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM client not available"
        )
    return client

# --- Answer about VNS Policy ---
@router.post("/demo", summary="Generate answer about VNS policy using LLM and Meilisearch context")
def get_demo_answer(request: AskModel):
    query_vector = embedder_1.embedding(request.query)

    # Search Meilisearch Context
    context_data = meili_client.index('demo').search(
        request.query,
        {
            'vector': query_vector,
            'hybrid': {
                "embedder": "embedder",
                "semanticRatio": 0.5
            },
            'limit': 5
        }
    )

    # Prepare Prompt and Generate Answer
    content = DemoAnswerGeneration.create_message_content(
        context_data, request.query, request.history
    )
    completion = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": content}]
    )

    model_response = json.loads(completion.choices[0].message.content)

    return {
        'answer': model_response["answer"],
        'metadata': {
            "answer_source": model_response["source"],
            "search_result": context_data,
            "search_query": {
                'hybrid': {
                    "embedder": "embedder",
                    "semanticRatio": 0.5
                },
                'limit': 5
            },
        }
    }

# --- Answer about Agriculture ---
@router.post("/agriculture", summary="Generate answer about agriculture using LLM and Meilisearch context")
def get_agriculture_answer(request: AskModel):
    query_vector = embedder_1.embedding(request.query)

    # Search Meilisearch Context
    context_data = meili_client.index('agri_chatbot_v2').search(
        request.query,
        {
            'vector': query_vector,
            'hybrid': {
                "embedder": "embedder",
                "semanticRatio": 0.5
            },
            'limit': 5
        }
    )

    # Prepare Prompt and Generate Answer
    content = AgricultureAnswerGeneration.create_message_content(
        context_data, request.query, request.history
    )
    completion = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": content}]
    )
    model_response = json.loads(completion.choices[0].message.content)

    return {
        'answer': model_response['answer'],
        'metadata': {
            "answer_source": model_response['source'],
            "search_result": context_data,
            "search_query": {
                'hybrid': {
                    "embedder": "embedder",
                    "semanticRatio": 0.5
                },
                'limit': 5
            },
        }
    }
