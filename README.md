# PDF-Genie-Web
GDgoC 401 Study (Vibe Coding Project)
---
## **추천 기술 스택**

**FastAPI(백엔드) + React(프론트) + ChromaDB(벡터DB)** 조합이 가장 검증된 스택입니다. 실제로 이 구성으로 만들어진 PDF Q&A 프로젝트들이 GitHub에 다수 있어요.

| **레이어** | **기술** | **이유** |
| --- | --- | --- |
| **프론트엔드** | React + Vite | 빠른 개발, 반응형 쉬움 |
| **백엔드** | FastAPI (Python) | RAG 라이브러리 Python 생태계가 압도적 |
| **LLM** | OpenAI API / Gemini API | 키 발급 즉시 사용 가능 |
| **벡터DB** | ChromaDB | 로컬 내장형, 설정 거의 없음 |
| **PDF 파싱** | LangChain + PyPDF | 청킹·임베딩 파이프라인 한 번에 |
| **배포 (프론트)** | Vercel | GitHub 연동 후 자동 배포, 무료 |
| **배포 (백엔드)** | Render | Python 백엔드 무료 티어 지원 |

> **⚠️ Vercel은 서버리스 함수 실행 시간 제한이 있어서 RAG 백엔드는 Render에 따로 올리는 게 안전합니다.**
> 

## **2달 개발 로드맵**

- **1~2주차:** 환경 세팅 + FastAPI로 PDF 업로드 & 파싱 API 완성
- **3~4주차:** ChromaDB 연동 + 질문-답변 RAG 파이프라인 구현
- **5~6주차:** React 프론트 개발 (PDF 업로드 UI + 채팅 UI)
- **7주차:** Vercel + Render 배포 연결 및 테스트
- **8주차:** 버그 수정 + README + 발표 자료 정리
