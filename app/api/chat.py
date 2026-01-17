from fastapi import APIRouter
from app.schemas.question import ChatRequest
from app.rag import rag_answer

router = APIRouter()

@router.post("/")
def chat(req: ChatRequest):
    answer, sources = rag_answer(req.question)
    return {
        "answer": answer,
        "sources": sources
    }