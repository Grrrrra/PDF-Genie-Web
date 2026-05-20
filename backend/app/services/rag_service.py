from langchain_ollama import ChatOllama
from app.services.vector_service import get_vectorstore
from app.services.web_search_service import search_web
from app.services.query_service import classify_question_type, rewrite_web_query, preprocess_umask_hint
from app.services.prompt_service import build_answer_format

# LLM — 모듈 로드 시 1회만 초기화
llm = ChatOllama(
    model="gemma3:4b",
    temperature=0.1
)

# ← query = preprocess_umask_hint(query) 이 줄 삭제

_BLOCKED_DOMAINS = {
    "tenforums.com", "namu.wiki", "namuwiki.mirror.wiki",
    "reddit.com", "quora.com", "answers.com",
    "youtube.com", "facebook.com", "twitter.com",
    "amazon.com", "ebay.com", "aliexpress.com",
}


def _is_valid_web_result(item: dict, query_keywords: list[str]) -> bool:
    href = item.get("href", "").lower()
    title = item.get("title", "").lower()
    body = item.get("body", "").lower()

    for domain in _BLOCKED_DOMAINS:
        if domain in href:
            return False

    combined = title + " " + body
    return any(kw.lower() in combined for kw in query_keywords)


def ask_question(query: str, use_web: bool = True):

    # ── 0. 질문 전처리 (umask 등 계산 힌트 주입) ──
    query = preprocess_umask_hint(query)  # ← 여기로 이동

    # ── 1. 질문 분류 ──────────────────────────────
    question_type = classify_question_type(query)
    answer_format = build_answer_format(question_type)

    # ── 2. PDF 벡터 검색 ──────────────────────────
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 4,
            "fetch_k": 12,
            "lambda_mult": 0.7
        }
    )
    docs = retriever.invoke(query)

    # 중복 제거
    unique_docs = []
    seen = set()
    for doc in docs:
        key = (
            doc.metadata.get("source"),
            doc.metadata.get("page"),
            doc.metadata.get("chunk_index")
        )
        if key not in seen:
            seen.add(key)
            unique_docs.append(doc)

    pdf_context = "\n\n".join([
        f"[PDF p.{doc.metadata.get('page', '?')+1}] {doc.page_content}"
        for doc in unique_docs
    ])

    pdf_pages = sorted({
        doc.metadata["page"] + 1
        for doc in unique_docs
        if isinstance(doc.metadata.get("page"), int)
    })

    # ── 3. 웹 검색 + 관련도 필터링 ───────────────
    web_results: list[dict] = []
    web_context = "웹 검색 사용 안 함"

    if use_web:
        try:
            web_query = rewrite_web_query(query, question_type)

            # 관련도 필터에 쓸 핵심 키워드 추출 (영문 쿼리 단어 기준)
            query_keywords = [w for w in web_query.split() if len(w) > 2]

            raw_results = search_web(web_query, max_results=6)  # 여유있게 가져옴
            web_results = [
                item for item in raw_results
                if _is_valid_web_result(item, query_keywords)
            ][:3]  # 최종 3개만 사용

            if web_results:
                web_context = "\n\n".join([
                    f"제목: {item['title']}\n내용: {item['body']}\n링크: {item['href']}"
                    for item in web_results
                ])
            else:
                web_context = "관련된 웹 검색 결과 없음"

        except Exception as e:
            print(f"[RAG WEB SEARCH ERROR] {e}")
            web_results = []
            web_context = "웹 검색 중 오류 발생"

    # ── 4. LLM 프롬프트 생성 ──────────────────────
    prompt = f"""
너는 사용자의 PDF 문서를 기반으로 질문에 답변하는 전문 도우미다.

[절대 규칙]
1. PDF 내용이 있으면 반드시 PDF를 최우선으로 사용해라.
2. 웹 검색 결과는 PDF에 없는 내용을 보충할 때만 사용해라.
3. 질문과 관련 없는 PDF 문단은 답변에 포함하지 마라.
4. 질문과 관련 없는 웹 결과(다운로드 링크, 포럼 목록, 쇼핑몰 등)는 절대 언급하지 마라.
5. PDF 원문을 그대로 복사하지 말고 이해한 내용을 정리해서 답변해라.
6. 답변에서 참고한 PDF 페이지 번호를 자연스럽게 언급해라.
7. PDF와 웹 모두 관련 내용이 없으면 "문서에서 해당 내용을 찾을 수 없습니다."라고 답해라.

[수치 / 계산 / 알고리즘 규칙]

8. 비트 연산, 파일 권한, 메모리 주소, 알고리즘 계산이 포함된 질문은 반드시 단계별로 계산 과정을 보여줘라.
9. umask 계산은 반드시 AND NOT 비트 연산을 사용해라.
   공식: 실제권한 = 요청권한 & (~umask)
   예시: umask(022) → 0666 & ~022 = 0666 & 0755 = 0644
   절대 빼기(-) 연산으로 계산하지 마라.
10. 8진수 권한 표기(예: 0644, 0755)는 반드시 rwx 문자열로도 함께 표기해라.
    예시: 0644 → rw-r--r--
11. 스케줄링 알고리즘(FCFS, SJF, RR 등) 계산은 간트 차트 형식으로 순서를 표시해라.
12. 메모리 계산(페이지 테이블, 주소 변환 등)은 공식 → 대입 → 결과 순서로 단계를 나눠 보여줘라.
13. 수식이나 계산 결과가 포함된 답변은 틀린 값보다 "계산 불확실"이라고 표시하는 게 낫다.
    확신이 없는 수치는 "~로 추정" 또는 "PDF에서 확인 필요"라고 명시해라.

{answer_format}

질문 유형: {question_type}
질문: {query}

[PDF 참고 자료]
{pdf_context}

[웹 보충 자료]
{web_context}
""".strip()

    response = llm.invoke(prompt)

    # ── 5. 응답 반환 ──────────────────────────────
    return {
        "question_type": question_type,
        "answer": response.content,
        "pdf_pages": pdf_pages,
        "pdf_sources": [
            {
                "source": doc.metadata.get("source"),
                "page": doc.metadata.get("page"),
                "chunk_index": doc.metadata.get("chunk_index")
            }
            for doc in unique_docs
        ],
        "web_sources": web_results
    }