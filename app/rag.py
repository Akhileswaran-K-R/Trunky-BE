import pdfplumber
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.core.ai import ask_ai   # ✅ IMPORT HERE

PDF_PATH = "app/data/document.pdf"

model = SentenceTransformer("all-MiniLM-L6-v2")

chunks = []
index = None


def load_pdf():
    global chunks, index

    text = ""
    with pdfplumber.open(PDF_PATH) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    size = 500
    overlap = 100
    chunks = [
        text[i:i + size]
        for i in range(0, len(text), size - overlap)
    ]

    embeddings = model.encode(chunks).astype("float32")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)


def rag_answer(question: str):
    q_emb = model.encode([question]).astype("float32")
    D, I = index.search(q_emb, 3)

    context = "\n\n".join(chunks[i] for i in I[0])

    prompt = f"""
Answer using ONLY the context below.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question:
{question}
"""

    answer = ask_ai(prompt)  

    sources = [
        {
            "text": chunks[i],
            "score": float(D[0][j]),
            "source": "document.pdf"
        }
        for j, i in enumerate(I[0])
    ]

    return answer, sources
