// src/components/AnswerPanel.tsx

import SourceCard from "./SourceCard";
import { type AskResult } from "../api";

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
                whiteSpace: "pre-wrap",
                lineHeight: 1.8,
                fontSize: 15,
                color: "#28251d",
            }}>
                {answer}
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