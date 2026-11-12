import json
import os
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class Retriever:
    """FAISS vector retriever with semantic embeddings."""

    def __init__(self, index_dir: str | Path = "index", embedding_model: str = None):
        index_path = Path(index_dir)

        # Load chunks
        chunks_file = index_path / "chunks.json"
        if not chunks_file.exists():
            raise FileNotFoundError(
                f"Index not found at {chunks_file}. Run 'python src/rag/ingest.py' first."
            )

        self.records = json.loads(chunks_file.read_text(encoding="utf-8"))

        # Load or initialize embedding model
        self.embedding_model_name = embedding_model or os.getenv(
            "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
        )
        print(f"Loading embedding model: {self.embedding_model_name}")
        self.encoder = SentenceTransformer(self.embedding_model_name)

        # Load or create FAISS index
        index_file = index_path / "faiss.index"
        if index_file.exists():
            print(f"Loading existing FAISS index from {index_file}")
            self.index = faiss.read_index(str(index_file))
        else:
            print("Building new FAISS index...")
            self._build_index(index_path)

    def _build_index(self, index_path: Path):
        """Build FAISS index from chunks."""
        texts = [rec["text"] for rec in self.records]
        embeddings = self.encoder.encode(texts, show_progress_bar=True, convert_to_numpy=True)

        # Normalize for cosine similarity
        faiss.normalize_L2(embeddings)

        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # Inner product = cosine similarity after normalization
        self.index.add(embeddings.astype('float32'))

        # Save index
        index_file = index_path / "faiss.index"
        faiss.write_index(self.index, str(index_file))
        print(f"FAISS index saved to {index_file}")

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """Search for top-k most relevant chunks."""
        # Encode query
        query_embedding = self.encoder.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)

        # Search
        scores, indices = self.index.search(query_embedding.astype('float32'), top_k)

        # Build results
        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx < len(self.records):
                rec = self.records[idx]
                results.append({**rec, "score": round(float(score), 4)})

        return results


if __name__ == "__main__":
    retriever = Retriever()
    results = retriever.search("How is long term capital gain on listed shares taxed?", top_k=3)
    for hit in results:
        print(f"[{hit['doc']} p.{hit['page']} score={hit['score']}]\n{hit['text'][:200]}\n---")
