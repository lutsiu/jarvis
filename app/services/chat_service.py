from collections.abc import Generator

from sqlalchemy.orm import Session

from app.ai.openai_client import generate_answer, stream_answer
from app.models.conversation import Conversation
from app.models.message import Message

def handle_chat_message(
    db: Session,
    message: str,
    conversation_id: int | None = None,
) -> tuple[int, str]:
    if conversation_id is None:
        conversation = Conversation(title=message[:50])
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
    else:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()

        if conversation is None:
            raise ValueError("Conversation not found")

    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=message,
    )

    db.add(user_message)
    db.commit()

    previous_messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation.id)
        .order_by(Message.created_at.asc())
        .limit(20)
        .all()
    )

    openai_messages = [
        {
            "role": msg.role,
            "content": msg.content,
        }
        for msg in previous_messages
    ]

    answer = generate_answer(openai_messages)

    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=answer,
    )

    db.add(assistant_message)
    db.commit()

    return conversation.id, answer

def handle_stream_chat_message(
    db: Session,
    message: str,
    conversation_id: int | None = None,
) -> Generator[str, None, None]:
    if conversation_id is None:
        conversation = Conversation(title=message[:50])
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
    else:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()

        if conversation is None:
            raise ValueError("Conversation not found")

    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=message,
    )

    db.add(user_message)
    db.commit()

    previous_messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation.id)
        .order_by(Message.created_at.desc())
        .limit(20)
        .all()
    )

    previous_messages = list(reversed(previous_messages))

    openai_messages = [
        {
            "role": msg.role,
            "content": msg.content,
        }
        for msg in previous_messages
    ]

    full_answer = ""

    yield f"event: conversation_id\ndata: {conversation.id}\n\n"

    for chunk in stream_answer(openai_messages):
        full_answer += chunk
        yield f"event: token\ndata: {chunk}\n\n"

    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=full_answer,
    )

    db.add(assistant_message)
    db.commit()

    yield "event: done\ndata: [DONE]\n\n"