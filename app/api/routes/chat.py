from fastapi import APIRouter, HTTPException

from app.ai.openai_client import generate_answer
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):
  try: 
    answer = generate_answer(request.message)
    return ChatResponse(answer=answer)
  
  except Exception as error: 
    raise HTTPException(
      status_code=500,
      default=f"AI response generation failed: {str(error)}",
    )
  