from pydantic import BaseModel, Field


class MemoryCreateRequest(BaseModel):
    content: str = Field(..., min_length=1)
    category: str = "general"


class MemoryResponse(BaseModel):
    id: int
    content: str
    category: str

    class Config:
        from_attributes = True