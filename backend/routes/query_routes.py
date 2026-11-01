
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
import uuid

from services.vector_db import search_chunks
from services.ollama_service import generate_answer
from services.vision_service import generate_vision_answer

router = APIRouter()

IMAGE_FOLDER = Path("data/chat_images")


class QueryRequest(BaseModel):
    question: str = ""
    image_id: str | None = None


@router.post("/query")
def query(request: QueryRequest):

    question = request.question.strip()

    # CASE 1: Image question
    if request.image_id:

        try:
            image_id = str(uuid.UUID(request.image_id))
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid image ID"
            )

        # Find image using its generated UUID
        image_path = None

        for extension in [".jpg", ".png", ".webp"]:
            candidate = IMAGE_FOLDER / f"{image_id}{extension}"

            if candidate.is_file():
                image_path = candidate
                break

        if image_path is None:
            raise HTTPException(
                status_code=404,
                detail="Uploaded image not found"
            )

        if not question:
            question = "Describe this image accurately."

        try:
            answer = generate_vision_answer(
                str(image_path),
                question
            )

            return {
                "answer": answer,
                "type": "image",
                "sources": []
            }

        except Exception as error:
            print("Vision error:", error)

            raise HTTPException(
                status_code=500,
                detail="Unable to process image. Check Ollama and the vision model."
            )

    # CASE 2: Normal text-based PDF question
    if not question:
        raise HTTPException(
            status_code=400,
            detail="Please enter a question or upload an image"
        )

    try:
        context, sources = search_chunks(question)

        answer = generate_answer(
            question,
            context
        )

        return {
            "answer": answer,
            "type": "text",
            "sources": sources
        }

    except Exception as error:
        print("Text RAG error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to generate an answer"
        )
