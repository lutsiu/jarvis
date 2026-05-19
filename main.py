from fastapi import FastAPI

from app.api.routes.chat import router as chat_router
from app.db.database import Base, engine
from app.models.conversation import Conversation
from app.models.message import Message
from app.api.routes.memory import router as memory_router
from app.models.memory import Memory
from app.models.document import Document
from app.api.routes.documents import router as documents_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Jarvis API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(chat_router, prefix="/api")
app.include_router(memory_router, prefix="/api")
app.include_router(documents_router, prefix="/api")