import json
from fastapi import HTTPException
from core.clients.groq import model_name
from core.clients.meilisearch import MeiliClient as meili_client
from core.agents.prompts.content import AgricultureAnswerGeneration, DemoAnswerGeneration
from core.embedders import embedder_1
from apis.models.ask import AskModel

SEARCH_PARAMS = {
    'hybrid': {
        "embedder": "embedder",
        "semanticRatio": 0.5
    },
    'limit': 5
}

def _search_context(index_name: str, query: str):
    query_vector = embedder_1.embedding(query)
    return meili_client.index(index_name).search(query, {**SEARCH_PARAMS, 'vector': query_vector})

def generate_answer_with_index(index_name: str, request: AskModel, client: object):
    context_data = _search_context(index_name, request.query)
    
    # Select prompt generator based on index name
    if index_name in ['demo', 'vns_policy']:
        prompt_generator = DemoAnswerGeneration
    elif index_name in ['agri_chatbot_v2', 'agri_chatbot']:
        prompt_generator = AgricultureAnswerGeneration
    else:
        raise HTTPException(status_code=400, detail=f"No prompt generator found for index '{index_name}'")
    
    content = prompt_generator.create_message_content(context_data, request.query, request.history)

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
            "search_query": SEARCH_PARAMS,
        }
    }
