from fastapi import APIRouter
from pydantic import BaseModel
from services.rag import answer_query

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    semester: str
    subject: str
    model: str

@router.post("/chat/")
async def chat(request: QueryRequest):
    return await answer_query(request.question, request.semester, request.subject, request.model)
