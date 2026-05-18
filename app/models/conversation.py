from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class Conversation(Base):
  __tablename__ = "conversations"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  title: Mapped[str] = mapped_column(String(255), default="New Chat")
  created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
  updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
  
  messages = relationship(
    "Message", 
    back_populates="conversation",
    cascade="all, delete-orphan"
  )

