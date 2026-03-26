from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_service import parse_pdf

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="PDF 파일만 업로드 가능합니다.")
    
    contents = await file.read()
    text = parse_pdf(contents)
    
    return {
        "filename": file.filename,
        "total_chars": len(text),
        "preview": text[:500]
    }