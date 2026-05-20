# backend/app/services/web_search_service.py

import re
from duckduckgo_search import DDGS


# ─────────────────────────────────────────
# 필터링 패턴
# ─────────────────────────────────────────

BAD_URL_PATTERNS = [
    "/forums", "/forum",
    "/download", "/downloads",
    "/login", "/signup", "/register",
    "search?", "search/",
    "/ads/", "/ad?",
    "youtube.com", "youtu.be",
    "twitter.com", "x.com",
    "facebook.com", "instagram.com",
    "linkedin.com",
    "amazon.com", "ebay.com",
]

BAD_TITLE_PATTERNS = [
    "download", "다운로드",
    "shop", "buy", "purchase",
    "login", "sign up",
    "forum list", "포럼",
]

GOOD_DOMAIN_BONUS = [
    "docs.", "doc.", "official",
    "github.com",
    "stackoverflow.com",
    "developer.",
    "wiki",
    "tutorial",
    "guide",
    "tistory.com",
    "velog.io",
    "medium.com",
    "geeksforgeeks.org",
    "man7.org",
    "linuxcommand.org",
]


# ─────────────────────────────────────────
# 필터 함수
# ─────────────────────────────────────────

def _is_valid_result(item: dict) -> bool:
    url   = (item.get("href") or "").lower()
    title = (item.get("title") or "").lower()
    body  = (item.get("body") or "").strip()

    if any(p in url for p in BAD_URL_PATTERNS):
        return False

    if any(p in title for p in BAD_TITLE_PATTERNS):
        return False

    if len(body) < 40:
        return False

    # 루트 도메인만 있는 URL 제거 (예: https://linux.org/)
    after_scheme = url.split("//")[-1]
    parts = after_scheme.split("/", 1)
    if len(parts) < 2 or parts[1].strip("/") == "":
        return False

    return True


def _score_result(question: str, item: dict) -> float:
    q_tokens = [t for t in re.split(r"[\s\?\.,!]+", question.lower()) if len(t) > 1]
    text = " ".join([
        item.get("title", ""),
        item.get("body", ""),
        item.get("href", ""),
    ]).lower()

    score = 0.0

    for token in q_tokens:
        if token in text:
            score += 2.0

    url = (item.get("href") or "").lower()
    for domain in GOOD_DOMAIN_BONUS:
        if domain in url:
            score += 1.5
            break

    body_len = len(item.get("body", ""))
    if body_len > 200:
        score += 1.0
    elif body_len > 100:
        score += 0.5

    return score


# ─────────────────────────────────────────
# 메인 검색 함수
# ─────────────────────────────────────────

def search_web(query: str, max_results: int = 3) -> list[dict]:
    """
    DuckDuckGo로 검색 → 필터 → 스코어 정렬 → 상위 max_results 반환
    반환 형식: [{"title": ..., "body": ..., "href": ...}]
    """
    try:
        raw_results = []
        with DDGS() as ddgs:
            search_results = ddgs.text(query, max_results=10)
            for item in search_results:
                raw_results.append({
                    "title": item.get("title", ""),
                    "body":  item.get("body", ""),
                    "href":  item.get("href", ""),
                })
    except Exception as e:
        print(f"[WEB SEARCH ERROR] {e}")
        return []

    # 필터링
    filtered = [r for r in raw_results if _is_valid_result(r)]

    # 점수 정렬
    scored = sorted(filtered, key=lambda r: _score_result(query, r), reverse=True)

    return scored[:max_results]