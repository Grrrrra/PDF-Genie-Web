// src/components/SourceCard.tsx

interface SourceCardProps {
    title: string;
    body: string;
    href: string;
}

export default function SourceCard({ title, body, href }: SourceCardProps) {
    let hostname = href;
    try {
        hostname = new URL(href).hostname;
    } catch {
        hostname = href;
    }

    return (
        <div style={{
            border: "1px solid #ddd",
            borderRadius: 8,
            padding: "12px 16px",
            marginBottom: 10,
            background: "#fafafa",
        }}>
            <a
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                style={{
                    fontWeight: 600,
                    color: "#01696f",
                    textDecoration: "none",
                    fontSize: 14,
                }}
            >
                {title}
            </a>
            <p style={{
                marginTop: 6,
                fontSize: 13,
                color: "#555",
                lineHeight: 1.5,
                display: "-webkit-box",
                WebkitLineClamp: 2,
                WebkitBoxOrient: "vertical",
                overflow: "hidden",
            }}>
                {body}
            </p>
            <span style={{ fontSize: 11, color: "#aaa" }}>{hostname}</span>
        </div>
    );
}