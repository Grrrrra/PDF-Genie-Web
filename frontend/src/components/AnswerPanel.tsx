// src/components/AnswerPanel.tsx

import ReactMarkdown from "react-markdown";
import SourceCard from "./SourceCard";
import type { AskResult } from "../api";

interface AnswerPanelProps {
    data: AskResult | null;
}

export default function AnswerPanel({ data }: AnswerPanelProps) {
    if (!data) return null;

    const { answer, pdf_sources, web_sources } = data;

    return (
        <div style={{ marginTop: 32 }}>

            {/* 답변 본문 */}
            <h2 style={{ marginBottom: 12 }}>답변</h2>
            <div style={{
                background: "#f7f6f2",
                borderRadius: 8,
                padding: "16px 20px",
                lineHeight: 1.8,
                fontSize: 15,
                color: "#28251d",
            }}>
                <ReactMarkdown
                    components={{
                        // 코드 블록 스타일
                        code({ children }) {
                            return (
                                <code style={{
                                    background: "#e8e6e0",
                                    borderRadius: 4,
                                    padding: "2px 6px",
                                    fontSize: 13,
                                    fontFamily: "monospace",
                                }}>
                                    {children}
                                </code>
                            );
                        },
                        // 코드 펜스 블록
                        pre({ children }) {
                            return (
                                <pre style={{
                                    background: "#1c1b19",
                                    color: "#cdccca",
                                    borderRadius: 6,
                                    padding: "12px 16px",
                                    overflowX: "auto",
                                    fontSize: 13,
                                    lineHeight: 1.6,
                                    margin: "10px 0",
                                }}>
                                    {children}
                                </pre>
                            );
                        },
                        // 강조 텍스트
                        strong({ children }) {
                            return (
                                <strong style={{ color: "#01696f" }}>
                                    {children}
                                </strong>
                            );
                        },
                        // 리스트 간격
                        ul({ children }) {
                            return (
                                <ul style={{ paddingLeft: 20, margin: "8px 0" }}>
                                    {children}
                                </ul>
                            );
                        },
                        li({ children }) {
                            return (
                                <li style={{ marginBottom: 4 }}>
                                    {children}
                                </li>
                            );
                        },
                    }}
                >
                    {answer}
                </ReactMarkdown>
            </div>

            {/* PDF 출처 */}
            <h3 style={{ marginTop: 28, marginBottom: 10 }}>📄 PDF 출처</h3>
            {pdf_sources?.length ? (
                <ul style={{ paddingLeft: 20, margin: 0 }}>
                    {pdf_sources.map((src, idx) => (
                        <li key={idx} style={{ marginBottom: 6, fontSize: 14, color: "#444" }}>
                            <strong>{src.source}</strong>
                            <span style={{ marginLeft: 8, color: "#01696f" }}>
                                p.{src.page + 1}
                            </span>
                            <span style={{ marginLeft: 8, color: "#aaa", fontSize: 12 }}>
                                chunk {src.chunk_index}
                            </span>
                        </li>
                    ))}
                </ul>
            ) : (
                <p style={{ color: "#aaa", fontSize: 14 }}>PDF 출처 없음</p>
            )}

            {/* 웹 출처 */}
            <h3 style={{ marginTop: 28, marginBottom: 10 }}>🌐 웹 출처</h3>
            {web_sources?.length ? (
                web_sources.map((src, idx) => (
                    <SourceCard
                        key={idx}
                        title={src.title}
                        body={src.body}
                        href={src.href}
                    />
                ))
            ) : (
                <p style={{ color: "#aaa", fontSize: 14 }}>웹 출처 없음</p>
            )}

        </div>
    );
}