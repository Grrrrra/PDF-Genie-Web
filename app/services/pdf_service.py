import pypdf
import tempfile
import os

def parse_pdf(file_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        reader = pypdf.PdfReader(tmp_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
    finally:
        os.unlink(tmp_path)

    return text