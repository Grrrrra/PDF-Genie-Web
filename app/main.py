from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import pdf

app = FastAPI(title="PDF Genie API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 나중에 React 연동 시 수정
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pdf.router, prefix="/pdf", tags=["PDF"])