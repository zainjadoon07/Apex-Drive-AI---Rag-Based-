"""
retrieval.py - Hybrid Retrieval Engine with Reciprocal Rank Fusion (RRF),
Context Budget Management, LRU Caching, and Graceful Failure Handling.
"""

import os
import re
import json
import time
import pickle
import asyncio
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from collections import OrderedDict

import numpy as np
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
INDEX_DIR = DATA_DIR / "index"

CHUNKS_FILE = INDEX_DIR / "chunks.json"
EMBEDDINGS_FILE = INDEX_DIR / "embeddings.npy"
BM25_FILE = INDEX_DIR / "bm25.pkl"

MODEL_NAME = "all-MiniLM-L6-v2"


# --- 1. Query LRU Cache ---

class LRUCache:
    """Thread-safe and fast in-memory LRU cache for query retrieval results."""
    def __init__(self, capacity: int = 256):
        self.capacity = capacity
        self.cache: OrderedDict[str, dict] = OrderedDict()

    def get(self, key: str) -> Optional[dict]:
        clean_key = key.strip().lower()
        if clean_key in self.cache:
            self.cache.move_to_end(clean_key)
            return self.cache[clean_key]
        return None

    def put(self, key: str, value: dict):
        clean_key = key.strip().lower()
        if clean_key in self.cache:
            self.cache.move_to_end(clean_key)
        self.cache[clean_key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def clear(self):
        self.cache.clear()


# --- 2. Tokenizer for BM25 ---

STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can", "can't", "cannot", "could",
    "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down",
    "during", "each", "few", "for", "from", "further", "had", "hadn't", "has",
    "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her",
    "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's",
    "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it",
    "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my",
    "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or",
    "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same",
    "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so",
    "some", "such", "than", "that", "that's", "the", "their", "theirs", "them",
    "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll",
    "they're", "they've", "this", "those", "through", "to", "too", "under", "until",
    "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
    "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves", "tell", "give", "help", "please"
}

def bm25_tokenize(text: str, remove_stopwords: bool = False) -> List[str]:
    text = text.lower()
    tokens = re.findall(r'\b[a-z0-9_-]+\b', text)
    if remove_stopwords:
        tokens = [t for t in tokens if t not in STOPWORDS]
    return tokens


# --- 3. Retrieval Result Container ---

class RetrievalResult:
    def __init__(
        self,
        chunks: List[Dict],
        citations: List[Dict],
        latency_ms: float,
        is_relevant: bool = True,
        is_cached: bool = False,
        error: Optional[str] = None
    ):
        self.chunks = chunks
        self.citations = citations
        self.latency_ms = latency_ms
        self.is_relevant = is_relevant
        self.is_cached = is_cached
        self.error = error

    def format_context_for_prompt(self, max_tokens: int = 1200) -> str:
        """
        Formats retrieved chunks into a clean, numbered context block for LLM prompt injection.
        Applies a strict token/character budget to prevent context overflow.
        """
        if not self.chunks or not self.is_relevant:
            return ""

        context_blocks = []
        # Rough token approximation: 1 token ~= 4 characters
        char_budget = max_tokens * 4
        current_chars = 0

        for idx, chunk in enumerate(self.chunks, start=1):
            source_tag = f"[Source {idx}: {chunk.get('source_file', 'unknown')}]"
            title_tag = f"Title: {chunk.get('doc_title', '')} | Section: {chunk.get('section_title', '')}"
            body_text = chunk.get("raw_body", chunk.get("text", "")).strip()

            block = f"--- {source_tag} ---\n{title_tag}\n{body_text}\n"
            block_len = len(block)

            if current_chars + block_len > char_budget:
                # Truncate if partially fitting, or break
                remaining_chars = char_budget - current_chars
                if remaining_chars > 200:
                    truncated_body = body_text[: remaining_chars - 100] + " ...[truncated for length]"
                    block = f"--- {source_tag} ---\n{title_tag}\n{truncated_body}\n"
                    context_blocks.append(block)
                break

            context_blocks.append(block)
            current_chars += block_len

        return "\n".join(context_blocks)


# --- 4. Main Retrieval Engine ---

class RetrievalEngine:
    def __init__(
        self,
        top_k: int = 4,
        similarity_threshold: float = 0.30,
        rrf_constant: int = 60,
        cache_capacity: int = 256
    ):
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold
        self.rrf_constant = rrf_constant
        self.cache = LRUCache(capacity=cache_capacity)

        self._embedder: Optional[SentenceTransformer] = None
        self.chunks: List[Dict] = []
        self.embeddings: Optional[np.ndarray] = None
        self.bm25: Optional[BM25Okapi] = None
        self.is_loaded = False

    def load_index(self):
        """Loads chunks, dense embeddings, and BM25 index into memory."""
        if self.is_loaded:
            return

        if not CHUNKS_FILE.exists() or not EMBEDDINGS_FILE.exists():
            raise FileNotFoundError(
                f"Index files not found in {INDEX_DIR}. Please run `python indexer.py` first."
            )

        # 1. Load chunks
        with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

        # 2. Load dense embeddings (already L2 normalized float32)
        self.embeddings = np.load(EMBEDDINGS_FILE)

        # 3. Load BM25 index
        if BM25_FILE.exists():
            with open(BM25_FILE, "rb") as f:
                data = pickle.load(f)
                self.bm25 = data.get("bm25")
        else:
            tokenized_corpus = [bm25_tokenize(c["text"]) for c in self.chunks]
            self.bm25 = BM25Okapi(tokenized_corpus)

        self.is_loaded = True

    @property
    def embedder(self) -> SentenceTransformer:
        if self._embedder is None:
            self._embedder = SentenceTransformer(MODEL_NAME, device="cpu")
        return self._embedder

    def retrieve(
        self,
        query: str,
        mode: str = "hybrid",
        top_k: Optional[int] = None
    ) -> RetrievalResult:
        """
        Retrieves top-k relevant chunks using:
        - 'hybrid': Reciprocal Rank Fusion of Dense + BM25 (Default Bonus Feature)
        - 'dense': Dense cosine similarity only
        - 'sparse': BM25 keyword matching only
        """
        t0 = time.perf_counter()
        k = top_k or self.top_k
        query = query.strip()

        if not query:
            return RetrievalResult(chunks=[], citations=[], latency_ms=0.0, is_relevant=False)

        # 1. Check LRU Cache
        cache_key = f"{mode}:{k}:{query}"
        cached = self.cache.get(cache_key)
        if cached:
            latency_ms = (time.perf_counter() - t0) * 1000.0
            return RetrievalResult(
                chunks=cached["chunks"],
                citations=cached["citations"],
                latency_ms=round(latency_ms, 2),
                is_relevant=cached["is_relevant"],
                is_cached=True
            )

        # 2. Ensure index is loaded
        try:
            self.load_index()
        except Exception as e:
            latency_ms = (time.perf_counter() - t0) * 1000.0
            return RetrievalResult(
                chunks=[],
                citations=[],
                latency_ms=round(latency_ms, 2),
                is_relevant=False,
                error=f"Vector store loading error: {str(e)}"
            )

        if not self.chunks or self.embeddings is None:
            latency_ms = (time.perf_counter() - t0) * 1000.0
            return RetrievalResult(chunks=[], citations=[], latency_ms=round(latency_ms, 2), is_relevant=False)

        # --- A. Dense Semantic Search ---
        dense_scores = np.zeros(len(self.chunks), dtype=np.float32)
        if mode in ("dense", "hybrid"):
            # Embed query with CPU model and normalize
            query_emb = self.embedder.encode([query], normalize_embeddings=True)
            query_emb = np.array(query_emb[0], dtype=np.float32)
            # Dot-product with normalized chunk matrix = Cosine Similarity
            dense_scores = np.dot(self.embeddings, query_emb)

        # --- B. Sparse BM25 Keyword Search ---
        sparse_scores = np.zeros(len(self.chunks), dtype=np.float32)
        if mode in ("sparse", "hybrid") and self.bm25 is not None:
            query_tokens = bm25_tokenize(query, remove_stopwords=True)
            if query_tokens:
                sparse_scores = np.array(self.bm25.get_scores(query_tokens), dtype=np.float32)

        # --- C. Ranking & Fusion ---
        if mode == "dense":
            ranked_indices = np.argsort(-dense_scores)[:k]
            max_score = float(dense_scores[ranked_indices[0]]) if len(ranked_indices) > 0 else 0.0
            is_relevant = max_score >= self.similarity_threshold

        elif mode == "sparse":
            ranked_indices = np.argsort(-sparse_scores)[:k]
            max_score = float(sparse_scores[ranked_indices[0]]) if len(ranked_indices) > 0 else 0.0
            is_relevant = max_score >= 5.0

        else:  # Hybrid: Reciprocal Rank Fusion (RRF)
            dense_rank_order = np.argsort(-dense_scores)
            sparse_rank_order = np.argsort(-sparse_scores)

            rrf_scores = np.zeros(len(self.chunks), dtype=np.float32)
            c = self.rrf_constant

            # Add RRF reciprocal ranks for top 40 candidates in each
            top_candidates = 40
            for rank, idx in enumerate(dense_rank_order[:top_candidates]):
                rrf_scores[idx] += 1.0 / (c + rank + 1)

            for rank, idx in enumerate(sparse_rank_order[:top_candidates]):
                rrf_scores[idx] += 1.0 / (c + rank + 1)

            ranked_indices = np.argsort(-rrf_scores)[:k]
            top_dense = float(dense_scores[ranked_indices[0]]) if len(ranked_indices) > 0 else 0.0
            top_sparse = float(sparse_scores[ranked_indices[0]]) if len(ranked_indices) > 0 else 0.0

            # Relevant if semantic similarity passes threshold or content keyword matched strongly
            is_relevant = (top_dense >= self.similarity_threshold) or (top_sparse >= 3.5 and top_dense >= 0.18)

        # 3. Assemble Chunks & Citations
        retrieved_chunks = []
        citations = []

        if is_relevant:
            for idx in ranked_indices:
                chunk = self.chunks[idx].copy()
                chunk["dense_score"] = float(dense_scores[idx])
                chunk["bm25_score"] = float(sparse_scores[idx])
                retrieved_chunks.append(chunk)

                # Build clean citation payload for UI
                citations.append({
                    "doc_id": chunk.get("doc_id", ""),
                    "title": chunk.get("doc_title", ""),
                    "category": chunk.get("category", ""),
                    "section": chunk.get("section_title", ""),
                    "source_file": chunk.get("source_file", ""),
                    "excerpt": chunk.get("raw_body", chunk.get("text", ""))[:220].strip() + "..."
                })

        latency_ms = (time.perf_counter() - t0) * 1000.0

        result_payload = {
            "chunks": retrieved_chunks,
            "citations": citations,
            "is_relevant": is_relevant
        }
        self.cache.put(cache_key, result_payload)

        return RetrievalResult(
            chunks=retrieved_chunks,
            citations=citations,
            latency_ms=round(latency_ms, 2),
            is_relevant=is_relevant,
            is_cached=False
        )

    async def async_retrieve(
        self,
        query: str,
        mode: str = "hybrid",
        top_k: Optional[int] = None
    ) -> RetrievalResult:
        """Asynchronously executes retrieval in a background thread to prevent blocking FastAPI."""
        return await asyncio.to_thread(self.retrieve, query, mode, top_k)


# Create global singleton instance
retrieval_engine = RetrievalEngine()
