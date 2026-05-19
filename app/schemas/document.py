from datetime import datetime

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    filename: str
    content_type: str
    file_path: str
    created_at: datetime

    class Config:
        from_attributes = True

class DocumentTextResponse(BaseModel):
    document_id: int
    filename: str
    text_preview: str