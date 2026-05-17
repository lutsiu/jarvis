from openai import OpenAI

from app.core.config import settings

client = OpenAI(api_key=settings.OPEN_API_KEY)

def generate_answer(message: str) -> str:
  response = client.responses.create(
    model=settings.OPEN_AI_MODEL,
    input=message
  )
  return response.output_text