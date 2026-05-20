def build_answer_format(question_type: str) -> str:
    if question_type == "definition":
        return """
답변 형식:
[문서 기반 정의]
- 용어의 의미
- 문서에서 설명하는 핵심 개념

[웹 보충 정보]
- 일반적인 정의
- 추가 배경지식

[간단 예시]
- 1~2개의 짧은 예시

[출처 요약]
- PDF 페이지
- 웹 참고 주제
"""
    elif question_type == "comparison":
        return """
답변 형식:
[문서 기반 비교]
- 항목 A
- 항목 B
- 차이점

[웹 보충 정보]
- 추가 차이점 또는 최신 정보

[출처 요약]
- PDF 페이지
- 웹 참고 주제
"""
    elif question_type == "example":
        return """
답변 형식:
[문서 기반 설명]
- 문서에서 확인된 개념 설명

[웹 보충 예시]
- 실제 사용 예시 2~3개

[주의사항]
- 초보자가 헷갈리기 쉬운 점 1~2개

[출처 요약]
- PDF 페이지
- 웹 참고 주제
"""
    elif question_type == "summary":
        return """
답변 형식:
[문서 기반 요약]
- 핵심 3줄 요약

[웹 보충 정보]
- 필요한 경우만 짧게 보충

[출처 요약]
- PDF 페이지
- 웹 참고 주제
"""
    else:
        return """
답변 형식:
[문서 기반 답변]
...

[웹 보충 정보]
...

[출처 요약]
...
"""