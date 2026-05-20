from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_service import save_uploaded_file, ingest_pdf, clear_vectorstore

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="PDF 파일만 업로드 가능합니다.")

    file_path, stored_name = save_uploaded_file(file)

    # 새 PDF 업로드 전 기존 청크 전체 초기화
    clear_vectorstore()

    result = ingest_pdf(file_path, file.filename)

    return {
        "message": "PDF 업로드 및 색인 완료",
        "stored_name": stored_name,
        "source": result["source"],
        "num_pages": result["num_pages"],
        "num_chunks": result["num_chunks"]
    }