from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.memory import MemoryCreateRequest, MemoryResponse
from app.services.memory_service import create_memory, get_recent_memories


router = APIRouter(prefix="/memories", tags=["Memories"])


@router.post("", response_model=MemoryResponse)
def add_memory(request: MemoryCreateRequest, db: Session = Depends(get_db)):
    return create_memory(
        db=db,
        content=request.content,
        category=request.category,
    )


@router.get("", response_model=list[MemoryResponse])
def list_memories(db: Session = Depends(get_db)):
    return get_recent_memories(db)