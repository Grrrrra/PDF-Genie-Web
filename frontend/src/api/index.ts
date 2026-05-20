// src/api/index.ts

const BASE_URL = "http://127.0.0.1:8000";

export interface UploadResult {
    message: string;
    stored_name: string;
    source: string;
    num_pages: number;
    num_chunks: number;
}

export interface PdfSource {
    source: string;
    page: number;
    chunk_index: number;
}

export interface WebSource {
    title: string;
    body: string;
    href: string;
}

export interface AskResult {
    question_type: string;
    answer: string;
    pdf_pages: number[];
    pdf_sources: PdfSource[];
    web_sources: WebSource[];
}

export async function uploadPdf(file: File): Promise<UploadResult> {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${BASE_URL}/pdf/upload`, {
        method: "POST",
        body: formData,
    });

    if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "PDF 업로드 실패");
    }
    return res.json();
}

export async function askQuestion(
    question: string,
    useWeb: boolean = true
): Promise<AskResult> {
    const res = await fetch(`${BASE_URL}/chat/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, use_web: useWeb }),
    });

    if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "질문 요청 실패");
    }
    return res.json();
}