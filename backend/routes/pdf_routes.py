from fastapi import APIRouter, UploadFile, File
import shutil
import os

from services.pdf_service import extract_text_from_pdf, chunk_text
from services.vector_db import store_chunks

router = APIRouter()

UPLOAD_FOLDER = "data/pdfs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(file_path)

    chunks = chunk_text(text)

    store_chunks(chunks , file.filename)

    return {
        "filename": file.filename,
        "chunks": len(chunks),
        "message": "Stored successfully in ChromaDB"
    }