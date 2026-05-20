from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag_service import ask_question

router = APIRouter()

class AskRequest(BaseModel):
    question: str
    use_web: bool = True

@router.post("/ask")
async def ask(req: AskRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="질문을 입력해주세요.")

    return ask_question(req.question, use_web=req.use_web)