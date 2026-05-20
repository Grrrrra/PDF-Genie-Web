# backend/app/services/query_service.py

import re
from app.services.keyword_map import KEYWORD_MAP


# ─────────────────────────────────────────
# 질문 유형 분류
# ─────────────────────────────────────────
def preprocess_umask_hint(query: str) -> str:
    """umask 관련 질문이면 단계별 계산 결과를 쿼리에 직접 주입"""
    if "umask" not in query.lower():
        return query

    match = re.search(r"umask\s*\(?\s*0?([0-7]{1,3})\s*\)?", query)
    if not match:
        return query

    val = int(match.group(1), 8)           # 8진수 파싱
    default_file = 0o666                   # 일반 파일 기본 권한
    default_dir  = 0o777                   # 디렉토리 기본 권한

    result_file = default_file & (~val & 0o777)
    result_dir  = default_dir  & (~val & 0o777)

    def to_rwx(mode: int) -> str:
        bits = ["r", "w", "x"]
        result = ""
        for shift in [6, 3, 0]:
            for i, bit in enumerate(bits):
                result += bit if (mode >> (shift + (2 - i))) & 1 else "-"
        return result

    hint = f"""
[umask 계산 결과 — 반드시 아래 값을 그대로 사용해라]
umask 값     : {oct(val)} ({val:03b} {(val>>3 & 7):03b} {(val & 7):03b})
AND NOT 공식 : 실제권한 = 요청권한 & (~umask)
~umask       : ~{oct(val)} = {oct(~val & 0o777)}

일반 파일 (기본 0666):
  0666 & {oct(~val & 0o777)} = {oct(result_file)} → {to_rwx(result_file)}

디렉토리 (기본 0777):
  0777 & {oct(~val & 0o777)} = {oct(result_dir)} → {to_rwx(result_dir)}

위 결과가 정답이다. 절대 빼기(-) 연산을 사용하지 마라.
"""
    return query + hint

def classify_question_type(question: str) -> str:
    q = question.lower().strip()

    if any(word in q for word in [
        "무엇", "뭐야", "란", "정의", "설명해줘", "알려줘", "이란", "뭔가", "what is"
    ]):
        return "definition"
    if any(word in q for word in [
        "차이", "비교", "장단점", "vs", "versus", "다른점", "같은점", "compare"
    ]):
        return "comparison"
    if any(word in q for word in [
        "예시", "예를", "사용법", "실습", "코드", "어떻게", "how to", "example", "usage"
    ]):
        return "example"
    if any(word in q for word in [
        "요약", "정리", "핵심", "summary", "overview"
    ]):
        return "summary"

    return "general"


# ─────────────────────────────────────────
# 질문 유형별 쿼리 접미사
# ─────────────────────────────────────────

TYPE_SUFFIX: dict[str, str] = {
    "definition": "meaning explanation",
    "comparison": "comparison differences",
    "example":    "examples usage tutorial",
    "summary":    "overview summary",
    "general":    "",
}


# ─────────────────────────────────────────
# 불필요 어절 / 조사 제거 패턴
# ─────────────────────────────────────────

NOISE_PATTERN = re.compile(
    r"(이란\??|무엇인가\??|무엇인지|설명해줘|알려줘|에 대해|에대해"
    r"|정의|이란 무엇|가 뭔가\??|는 무엇\??|뭐야\??|이 뭔가\??)"
)
JOSA_PATTERN = re.compile(r"(이|가|은|는|을|를|의|에|으로|로)\s*$")

# 키워드 맵 — 긴 키워드 우선 정렬 (모듈 로드 시 1회만 계산)
_SORTED_KEYS = sorted(KEYWORD_MAP.keys(), key=len, reverse=True)


# ─────────────────────────────────────────
# 웹 검색어 리라이트
# ─────────────────────────────────────────

def rewrite_web_query(question: str, question_type: str) -> str:
    """
    질문을 검색 엔진에 최적화된 키워드로 변환.
    1) KEYWORD_MAP 탐색 (긴 키워드 우선)
    2) 매핑 없으면 노이즈/조사 제거 후 원문 사용
    3) question_type 접미사 추가
    """
    q_lower = question.lower().strip()

    # 1) 키워드 맵 탐색
    base_query = None
    for keyword in _SORTED_KEYS:
        if keyword in q_lower:
            base_query = KEYWORD_MAP[keyword]
            break

    # 2) 매핑 없으면 정제
    if not base_query:
        cleaned = NOISE_PATTERN.sub("", question).strip()
        cleaned = JOSA_PATTERN.sub("", cleaned).strip()
        base_query = cleaned[:60] if cleaned else question[:60]

    # 3) 접미사 추가
    suffix = TYPE_SUFFIX.get(question_type, "")
    return f"{base_query} {suffix}".strip() if suffix else base_query.strip()