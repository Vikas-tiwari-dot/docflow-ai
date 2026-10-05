import io, re, hashlib, logging
from pypdf import PdfReader
from docx import Document as DocxDocument
logger=logging.getLogger("docflow.processor")
ALLOWED={"application/pdf":"pdf","application/vnd.openxmlformats-officedocument.wordprocessingml.document":"docx"}

def normalize(text):
    text=re.sub(r"\r\n?","\n",text)
    text=re.sub(r"[ \t]+"," ",text)
    text=re.sub(r"\n{3,}","\n\n",text)
    return text.strip()

def extract(content: bytes, file_type: str):
    if file_type=="pdf":
        reader=PdfReader(io.BytesIO(content)); return normalize("\n".join((p.extract_text() or "") for p in reader.pages))
    if file_type=="docx":
        doc=DocxDocument(io.BytesIO(content)); return normalize("\n".join(p.text for p in doc.paragraphs))
    raise ValueError("Unsupported file type")

def sha256(content): return hashlib.sha256(content).hexdigest()
def chunk_text(text, size=5000):
    words=text.split(); chunks=[]; current=[]; n=0
    for w in words:
        if n+len(w)+1>size and current:
            chunks.append(" ".join(current)); current=[]; n=0
        current.append(w); n+=len(w)+1
    if current: chunks.append(" ".join(current))
    return chunks
