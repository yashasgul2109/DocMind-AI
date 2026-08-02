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

    print("\n========== EXTRACTED TEXT ==========")
    print(text[:3000])          # First 3000 characters
    print("===================================")
    print(f"Characters extracted: {len(text)}")

    chunks = chunk_text(text)

    print(f"\nTotal Chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        print(f"\n------ CHUNK {i} ------")
        print(chunk[:500])

    store_chunks(chunks, file.filename)

    return {
        "filename": file.filename,
        "chunks": len(chunks),
        "message": "Stored successfully in ChromaDB"
    }