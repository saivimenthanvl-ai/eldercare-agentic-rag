import os, json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class RagStore:
    def __init__(self, index_dir: str):
        self.index_dir = index_dir
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.docs = []

    def load(self):
        idx_path = os.path.join(self.index_dir, "faiss.index")
        docs_path = os.path.join(self.index_dir, "docs.jsonl")
        self.index = faiss.read_index(idx_path)
        self.docs = []
        with open(docs_path, "r", encoding="utf-8") as f:
            for line in f:
                self.docs.append(json.loads(line))

    def search(self, query: str, k: int = 5):
        q = self.model.encode([query], normalize_embeddings=True).astype("float32")
        D, I = self.index.search(q, k)
        results = []
        for idx in I[0]:
            if idx < 0: 
                continue
            results.append(self.docs[idx])
        return results
