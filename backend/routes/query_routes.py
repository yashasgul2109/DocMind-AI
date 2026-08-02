from fastapi import APIRouter
from pydantic import BaseModel

from services.vector_db import search_chunks
from services.ollama_service import generate_answer

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
def query(request: QueryRequest):

    context, sources = search_chunks(request.question)

    answer = generate_answer(
        request.question,
        context
    )

    return {
        "answer": answer,
        "sources": sources
    }