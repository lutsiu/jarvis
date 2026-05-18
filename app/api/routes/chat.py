from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from app.db.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import handle_chat_message, handle_stream_chat_message

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        conversation_id, answer = handle_chat_message(
            db=db,
            message=request.message,
            conversation_id=request.conversation_id,
        )

        return ChatResponse(
            conversation_id=conversation_id,
            answer=answer,
        )

    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    
@router.post("/stream")
def stream_chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        return StreamingResponse(
            handle_stream_chat_message(
                db=db,
                message=request.message,
                conversation_id=request.conversation_id,
            ),
            media_type="text/event-stream",
        )

    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))    