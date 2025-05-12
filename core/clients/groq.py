from openai import OpenAI
from config.settings import settings

GroqClient = OpenAI(base_url=settings.groq_url, api_key=settings.groq_api_key)
model_name = settings.groq_model_name
