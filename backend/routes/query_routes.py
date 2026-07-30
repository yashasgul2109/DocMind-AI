from fastapi import APIRouter
from pydantic import BaseModel

from services.vector_db import search_chunks
from services.gemini_service import generate_answer

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
def query(request: QueryRequest):

    results = search_chunks(request.question)

    docs = results["documents"][0]

    context = "\n\n".join(docs)

    answer = generate_answer(
        request.question,
        context
    )

    return {
        "answer": answer,
        "sources": results["metadatas"][0]
    }