from fastapi import FastAPI

from app.api.routes.chat import router as chat_router

app = FastAPI(title="Jarvis API")

@app.get("/health")
def health_check():
  return {"status": "ok"}

app.include_router(chat_router, prefix="/api")