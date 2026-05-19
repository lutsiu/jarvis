import shutil
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session
from pypdf import PdfReader
from app.models.document import Document


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def save_document(db: Session, file: UploadFile) -> Document:
    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document = Document(
        filename=file.filename,
        content_type=file.content_type or "unknown",
        file_path=str(file_path),
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document

def extract_text_from_document(document: Document) -> str:
    file_path = Path(document.file_path)

    if not file_path.exists():
        raise FileNotFoundError("Uploaded file not found")

    if document.content_type == "text/plain" or file_path.suffix.lower() == ".txt":
        return file_path.read_text(encoding="utf-8")

    if document.content_type == "application/pdf" or file_path.suffix.lower() == ".pdf":
        reader = PdfReader(str(file_path))

        text_parts = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

        return "\n\n".join(text_parts)

    raise ValueError("Unsupported file type")