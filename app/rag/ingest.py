import os, json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

def chunk_text(text: str, max_chars: int = 800):
    chunks, buf = [], ""
    for line in text.splitlines():
        if len(buf) + len(line) + 1 > max_chars:
            if buf.strip():
                chunks.append(buf.strip())
            buf = line
        else:
            buf += "\n" + line
    if buf.strip():
        chunks.append(buf.strip())
    return chunks

def ingest(knowledge_dir: str, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    model = SentenceTransformer("all-MiniLM-L6-v2")

    docs = []
    for fn in os.listdir(knowledge_dir):
        if not fn.endswith((".md", ".txt")):
            continue
        path = os.path.join(knowledge_dir, fn)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        for i, ch in enumerate(chunk_text(text)):
            docs.append({"id": f"{fn}:{i}", "source": fn, "text": ch})

    emb = model.encode([d["text"] for d in docs], normalize_embeddings=True).astype("float32")

    index = faiss.IndexFlatIP(emb.shape[1])
    index.add(emb)

    faiss.write_index(index, os.path.join(out_dir, "faiss.index"))
    with open(os.path.join(out_dir, "docs.jsonl"), "w", encoding="utf-8") as f:
        for d in docs:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    ingest("./data/knowledge", "./data/index")
