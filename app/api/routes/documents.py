from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.document import Document
from app.schemas.document import DocumentResponse, DocumentTextResponse
from app.services.document_service import (
    extract_text_from_document,
    save_document,
)


router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return save_document(db=db, file=file)


@router.get("/{document_id}/text", response_model=DocumentTextResponse)
def get_document_text(
    document_id: int,
    db: Session = Depends(get_db),
):
    document = db.query(Document).filter(Document.id == document_id).first()

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        text = extract_text_from_document(document)

        return DocumentTextResponse(
            document_id=document.id,
            filename=document.filename,
            text_preview=text[:3000],
        )

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))