
from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid

router = APIRouter()

IMAGE_FOLDER = "data/chat_images"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

os.makedirs(IMAGE_FOLDER, exist_ok=True)

ALLOWED_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp"
}


@router.post("/image/upload")
async def upload_image(file: UploadFile = File(...)):

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, PNG and WEBP images are allowed"
        )

    image_bytes = await file.read(MAX_FILE_SIZE + 1)

    if len(image_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Image size cannot exceed 10 MB"
        )

    image_id = str(uuid.uuid4())
    extension = ALLOWED_TYPES[file.content_type]

    image_name = image_id + extension
    image_path = os.path.join(IMAGE_FOLDER, image_name)

    with open(image_path, "wb") as image_file:
        image_file.write(image_bytes)

    return {
        "image_id": image_id,
        "filename": file.filename,
        "image_path": image_path,
        "message": "Image uploaded successfully"
    }
