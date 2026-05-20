// src/App.tsx

import { useState } from "react";
import { uploadPdf, askQuestion, type UploadResult, type AskResult } from "./api";
import AnswerPanel from "./components/AnswerPanel";

export default function App() {
    const [file, setFile] = useState<File | null>(null);
    const [uploadInfo, setUploadInfo] = useState<UploadResult | null>(null);
    const [question, setQuestion] = useState<string>("");
    const [useWeb, setUseWeb] = useState<boolean>(true);
    const [answer, setAnswer] = useState<AskResult | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string>("");

    // ── PDF 업로드 ───────────────────────────────
    const handleUpload = async () => {
        if (!file) return;
        setLoading(true);
        setError("");
        try {
            const result = await uploadPdf(file);
            setUploadInfo(result);
            setAnswer(null);
        } catch (e: unknown) {
            setError(e instanceof Error ? e.message : "업로드 실패");
        } finally {
            setLoading(false);
        }
    };

    // ── 질문 요청 ────────────────────────────────
    const handleAsk = async () => {
        if (!question.trim()) {
            setError("질문을 입력해주세요.");
            return;
        }
        if (!uploadInfo) {
            setError("PDF를 먼저 업로드해주세요.");
            return;
        }
        setLoading(true);
        setError("");
        setAnswer(null);
        try {
            const result = await askQuestion(question, useWeb);
            setAnswer(result);
        } catch (e: unknown) {
            setError(e instanceof Error ? e.message : "질문 요청 실패");
        } finally {
            setLoading(false);
        }
    };

    // ── 키보드 Enter 제출 ────────────────────────
    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
            handleAsk();
        }
    };

    return (
        <div style={{
            maxWidth: 800,
            margin: "0 auto",
            padding: "40px 24px",
            fontFamily: "sans-serif",
        }}>
            <h1 style={{ margin: 0 }}>📄 PDF Genie</h1>
            <p style={{ color: "#666", marginTop: 6, marginBottom: 36 }}>
                PDF 기반 질문-답변 + 웹 보충형 RAG 데모
            </p>

            {/* ── PDF 업로드 섹션 ─────────────────── */}
            <section style={{ marginBottom: 36 }}>
                <h2 style={{ marginBottom: 10 }}>PDF 업로드</h2>

                <input
                    type="file"
                    accept="application/pdf"
                    onChange={(e) => {
                        setFile(e.target.files?.[0] ?? null);
                        setUploadInfo(null);
                        setAnswer(null);
                        setError("");
                    }}
                    style={{ display: "block", marginBottom: 10 }}
                />

                <button
                    onClick={handleUpload}
                    disabled={loading || !file}
                    style={{
                        padding: "8px 20px",
                        background: file ? "#01696f" : "#ccc",
                        color: "#fff",
                        border: "none",
                        borderRadius: 6,
                        cursor: file ? "pointer" : "not-allowed",
                        fontSize: 14,
                    }}
                >
                    {loading && !answer ? "업로드 중..." : "업로드"}
                </button>

                {/* 업로드 완료 정보 */}
                {uploadInfo && (
                    <div style={{
                        marginTop: 12,
                        padding: "10px 16px",
                        background: "#e6f4f1",
                        borderRadius: 6,
                        fontSize: 14,
                        color: "#01696f",
                    }}>
                        ✅ <strong>{uploadInfo.source}</strong> 업로드 완료
                        &nbsp;/&nbsp; 페이지 수: {uploadInfo.num_pages}
                        &nbsp;/&nbsp; 청크 수: {uploadInfo.num_chunks}
                    </div>
                )}
            </section>

            {/* ── 질문 섹션 ───────────────────────── */}
            <section>
                <h2 style={{ marginBottom: 10 }}>질문하기</h2>

                <textarea
                    rows={3}
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="질문을 입력하세요 (Ctrl+Enter로 제출)"
                    style={{
                        width: "100%",
                        padding: "10px 12px",
                        fontSize: 15,
                        borderRadius: 6,
                        border: "1px solid #ccc",
                        resize: "vertical",
                        boxSizing: "border-box",
                        outline: "none",
                    }}
                />

                {/* 웹 보충 체크박스 */}
                <label style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 8,
                    marginTop: 10,
                    fontSize: 14,
                    cursor: "pointer",
                    userSelect: "none",
                }}>
                    <input
                        type="checkbox"
                        checked={useWeb}
                        onChange={(e) => setUseWeb(e.target.checked)}
                    />
                    웹 보충 포함
                </label>

                <button
                    onClick={handleAsk}
                    disabled={loading}
                    style={{
                        marginTop: 12,
                        padding: "10px 28px",
                        background: loading ? "#ccc" : "#01696f",
                        color: "#fff",
                        border: "none",
                        borderRadius: 6,
                        fontSize: 15,
                        cursor: loading ? "not-allowed" : "pointer",
                    }}
                >
                    질문하기
                </button>

                {/* 로딩 스피너 */}
                {loading && (
                    <div style={{
                        display: "flex",
                        alignItems: "center",
                        gap: 10,
                        marginTop: 16,
                        color: "#01696f",
                        fontSize: 14,
                    }}>
                        <svg
                            width="18" height="18"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            style={{ animation: "spin 1s linear infinite" }}
                        >
                            <path d="M21 12a9 9 0 1 1-6.219-8.56" />
                        </svg>
                        답변 생성 중...
                        <style>{`
                            @keyframes spin {
                                from { transform: rotate(0deg); }
                                to { transform: rotate(360deg); }
                            }
                        `}</style>
                    </div>
                )}

                {/* 에러 메시지 */}
                {error && (
                    <p style={{ marginTop: 10, color: "#a12c7b", fontSize: 14 }}>
                        ⚠️ {error}
                    </p>
                )}
            </section>

            {/* ── 답변 + 출처 ─────────────────────── */}
            <AnswerPanel data={answer} />
        </div>
    );
}