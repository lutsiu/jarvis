from sqlalchemy.orm import Session

from app.models.memory import Memory


def create_memory(db: Session, content: str, category: str) -> Memory:
    memory = Memory(content=content, category=category)

    db.add(memory)
    db.commit()
    db.refresh(memory)

    return memory


def get_recent_memories(db: Session, limit: int = 10) -> list[Memory]:
    return (
        db.query(Memory)
        .order_by(Memory.created_at.desc())
        .limit(limit)
        .all()
    )