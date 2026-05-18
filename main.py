from fastapi import FastAPI

from app.api.routes.chat import router as chat_router
from app.db.database import Base, engine
from app.models.conversation import Conversation
from app.models.message import Message


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Jarvis API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(chat_router, prefix="/api")