import os
import shutil
from uuid import uuid4
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.services.vector_service import get_vectorstore

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def clear_vectorstore():
    """ChromaDB 컬렉션 전체 초기화 — 새 PDF 업로드 전 호출"""
    vectorstore = get_vectorstore()
    try:
        all_ids = vectorstore._collection.get()["ids"]
        if all_ids:
            vectorstore._collection.delete(ids=all_ids)
    except Exception as e:
        print(f"[clear_vectorstore] 초기화 실패: {e}")


def save_uploaded_file(upload_file):
    ext = os.path.splitext(upload_file.filename)[1]
    stored_name = f"{uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, stored_name)

    upload_file.file.seek(0)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return file_path, stored_name


def ingest_pdf(file_path: str, original_filename: str):
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = splitter.split_documents(docs)

    for i, chunk in enumerate(chunks):
        chunk.metadata["source"] = original_filename
        chunk.metadata["chunk_index"] = i

    vectorstore = get_vectorstore()
    vectorstore.add_documents(chunks)

    return {
        "source": original_filename,
        "num_pages": len(docs),
        "num_chunks": len(chunks)
    }