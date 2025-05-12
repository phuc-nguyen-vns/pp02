from openai import OpenAI
from openai.types import CreateEmbeddingResponse
from typing import List
from config.settings import settings

def embedding(text: str) -> List[float]:
    embedder_1_cf = settings.embedder_1

    # Ensure 'url' is just the base URL, without '/v1/embeddings'
    base_url = embedder_1_cf['url'].replace('/embeddings', '')
    print(base_url)

    # Create OpenAI SDK client
    client = OpenAI(base_url=base_url, api_key=embedder_1_cf['token'])

    try:
        response: CreateEmbeddingResponse = client.embeddings.create(
            input=text,  # Batch format required
            model=embedder_1_cf['model']
        )

        if not response.data:
            raise ValueError("No embedding data returned from the API.")

        return response.data[0].embedding

    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []

if __name__ == "__main__":
    text = "hello"
    emb = embedding(text)
    print(f"Embedding Vector Length: {len(emb)}")
    print(f"First 10 Values: {emb[:10]}")
