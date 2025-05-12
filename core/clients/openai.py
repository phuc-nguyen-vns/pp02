from openai import OpenAI
from config.settings import settings

# Initialize the OpenAI client
OpenAIClient = OpenAI(base_url=settings.openai_url, api_key=settings.openai_api_key)
model_name = settings.openai_model_name 

def generate_completion(prompt: str, max_tokens: int = 50) -> str:
    try:
        response = OpenAIClient.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error generating completion: {e}")
        return ""

if __name__ == "__main__":
    prompt_text = "Once upon a time"
    result = generate_completion(prompt_text)
    print(f"Generated Text:\n{result}")
