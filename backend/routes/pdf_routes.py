
from fastapi import APIRouter, UploadFile, File
import shutil
import os
from services.pdf_service import extract_pdf_content, chunk_text
from services.vector_db import store_chunks
from services.image_service import extract_images_from_pdf

router = APIRouter()

UPLOAD_FOLDER = "data/pdfs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save uploaded PDF
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    text = extract_pdf_content(file_path)

    print("\n========== EXTRACTED TEXT ==========")
    print(text[:3000])
    print("===================================")
    print(f"Characters extracted: {len(text)}")

    # Create text chunks
    chunks = chunk_text(text)

    print(f"\nTotal Chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        print(f"\n------ CHUNK {i} ------")
        print(chunk[:500])

    # Store text chunks in ChromaDB
    store_chunks(chunks, file.filename)

    # Extract images from PDF
    extracted_images = extract_images_from_pdf(
        file_path,
        file.filename
    )

    print(f"\nTotal Images Extracted: {len(extracted_images)}")

    for image in extracted_images:
        print(
            f"Image: {image['image_path']} | "
            f"Page: {image['page_number']}"
        )

    return {
        "filename": file.filename,
        "chunks": len(chunks),
        "images": len(extracted_images),
        "message": "PDF text and images processed successfully"
    }
