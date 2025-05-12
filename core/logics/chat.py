import json
from fastapi import HTTPException
from core.clients.groq import GroqClient as client, model_name
from core.clients.meilisearch import MeiliClient as meilisearch_client
from apis.v1.meilisearch_router import semantic_search, hybrid_search, keyword_search
from core.agents.prompts.content import AnswerGeneration, NextQuestionGeneration
from apis.models.chat import ChatGenerationModel


def _search_context(request: ChatGenerationModel):
    if request.search_type == "keyword":
        return keyword_search(request, meilisearch_client)
    elif request.search_type == "semantic":
        return semantic_search(request, meilisearch_client)
    elif request.search_type == "hybrid":
        return hybrid_search(request, meilisearch_client)
    else:
        raise HTTPException(status_code=400, detail="Invalid search_type")


def generate_answer(request: ChatGenerationModel, client: object):
    context_data = _search_context(request)
    context = "\n\n".join(hit["content"] for hit in context_data["hits"])

    prompt_content = AnswerGeneration.create_message_content(context, request.query, request.history)
    completion = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt_content}]
    )

    return completion.choices[0].message.content


def generate_next_question(request: ChatGenerationModel, client: object):
    context_data = _search_context(request)
    context = "\n\n".join(hit["content"] for hit in context_data["hits"])

    prompt_content = NextQuestionGeneration.create_message_content(context, request.query, request.history)
    print(client)
    print(model_name, "*"*100)
    completion = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt_content}]
    )

    return completion.choices[0].message.content
