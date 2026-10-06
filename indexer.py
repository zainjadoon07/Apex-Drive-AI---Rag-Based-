"""
indexer.py - Offline Indexing Pipeline for Apex Car Rental RAG Assistant

Features:
1. Heading-Aware Semantic Chunking: Parses markdown frontmatter and splits by headings.
2. Incremental Re-runnability: Tracks MD5 hashes of all documents in `doc_hashes.json`.
   Only re-chunks and re-embeds new or modified documents. Unchanged files are preserved.
3. CPU-Friendly Embeddings: Uses sentence-transformers 'all-MiniLM-L6-v2' (384-dim).
4. Dual Vector & Keyword Index:
   - Dense: L2-normalized float32 NumPy matrix for sub-millisecond cosine similarity.
   - Sparse: Tokenized BM25Okapi index for exact keyword and code/model matching.
5. Rich Metadata: Each chunk stores doc_id, title, category, section, filename, and text.
"""

import os
import re
import json
import time
import pickle
import hashlib
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional

import numpy as np
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = DATA_DIR / "documents"
INDEX_DIR = DATA_DIR / "index"
INDEX_DIR.mkdir(parents=True, exist_ok=True)

HASH_FILE = INDEX_DIR / "doc_hashes.json"
CHUNKS_FILE = INDEX_DIR / "chunks.json"
EMBEDDINGS_FILE = INDEX_DIR / "embeddings.npy"
BM25_FILE = INDEX_DIR / "bm25.pkl"

MODEL_NAME = "all-MiniLM-L6-v2"


# --- 1. Incremental Hash Tracker ---

def compute_file_md5(file_path: Path) -> str:
    """Computes MD5 checksum of a file for change detection."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def load_stored_hashes() -> Dict[str, str]:
    if HASH_FILE.exists():
        try:
            with open(HASH_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_stored_hashes(hashes: Dict[str, str]):
    with open(HASH_FILE, "w", encoding="utf-8") as f:
        json.dump(hashes, f, indent=2)


# --- 2. Markdown Parsing & Heading-Aware Semantic Chunking ---

def parse_frontmatter(content: str) -> Tuple[Dict[str, str], str]:
    """Extracts frontmatter metadata from markdown."""
    metadata = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1].strip()
            body = parts[2].strip()
            for line in fm_text.splitlines():
                if ":" in line:
                    key, val = line.split(":", 1)
                    metadata[key.strip()] = val.strip().strip('"').strip("'")
    return metadata, body

def chunk_markdown_document(file_path: Path) -> List[Dict]:
    """
    Splits a markdown document into semantic chunks using section headers.
    Keeps chunks between 150-400 words with metadata context prefix.
    """
    raw_content = file_path.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(raw_content)

    doc_id = metadata.get("id", file_path.stem)
    doc_title = metadata.get("title", file_path.stem.replace("_", " ").title())
    category = metadata.get("category", "General")
    filename = file_path.name

    # Split document by markdown headings (e.g. ## Heading)
    sections = re.split(r'\n(?=##?\s+)', body)
    chunks = []
    chunk_idx = 0

    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue

        # Extract section heading
        lines = sec.splitlines()
        first_line = lines[0].strip()
        section_title = "Overview"
        if first_line.startswith("#"):
            section_title = re.sub(r'^#+\s*', '', first_line).strip()

        words = sec.split()
        
        # If section is very long (> 350 words), chunk with sliding window
        max_words = 300
        overlap = 40
        if len(words) > max_words:
            start = 0
            while start < len(words):
                end = min(start + max_words, len(words))
                sub_words = words[start:end]
                sub_text = " ".join(sub_words)
                
                # Prepend contextual anchor header
                contextual_text = (
                    f"Document: {doc_title} | Category: {category} | Section: {section_title}\n"
                    f"{sub_text}"
                )
                chunk_id = f"{doc_id}_c{chunk_idx:02d}"
                chunks.append({
                    "chunk_id": chunk_id,
                    "doc_id": doc_id,
                    "doc_title": doc_title,
                    "category": category,
                    "section_title": section_title,
                    "source_file": filename,
                    "text": contextual_text,
                    "raw_body": sub_text
                })
                chunk_idx += 1
                if end == len(words):
                    break
                start += (max_words - overlap)
        else:
            # Short / normal section: keep as a single atomic chunk
            contextual_text = (
                f"Document: {doc_title} | Category: {category} | Section: {section_title}\n"
                f"{sec}"
            )
            chunk_id = f"{doc_id}_c{chunk_idx:02d}"
            chunks.append({
                "chunk_id": chunk_id,
                "doc_id": doc_id,
                "doc_title": doc_title,
                "category": category,
                "section_title": section_title,
                "source_file": filename,
                "text": contextual_text,
                "raw_body": sec
            })
            chunk_idx += 1

    return chunks


def chunk_pdf_document(file_path: Path) -> List[Dict]:
    """
    Extracts text from an enterprise PDF document using pypdf and splits into semantic chunks.
    """
    try:
        from pypdf import PdfReader
    except ImportError:
        raise ImportError("pypdf is required to index PDF documents. Install via `pip install pypdf`.")

    reader = PdfReader(str(file_path))
    pages_text = [page.extract_text() or "" for page in reader.pages]
    full_text = "\n".join(pages_text)

    # Extract metadata from header lines
    lines = [line.strip() for line in full_text.splitlines() if line.strip()]
    doc_id = file_path.stem
    doc_title = file_path.stem.replace("_", " ").title()
    category = "General"

    for line in lines[:10]:
        if "CATEGORY:" in line:
            category = line.split("CATEGORY:", 1)[1].strip()
        elif "Document ID:" in line:
            m = re.search(r"Document ID:\s*([A-Z0-9_-]+)", line)
            if m:
                doc_id = m.group(1)

    if len(lines) > 1 and not lines[1].startswith("Document ID") and not lines[1].startswith("CATEGORY:"):
        doc_title = lines[1]

    # Split by section headers (common pattern in our generated PDFs)
    sections = re.split(r'\n(?=[A-Z][A-Za-z0-9\s&,/-]{3,45}\n)', full_text)
    if len(sections) <= 1:
        sections = re.split(r'\n\n+', full_text)

    chunks = []
    chunk_idx = 0
    for sec in sections:
        sec = sec.strip()
        if not sec or len(sec.split()) < 8:
            continue

        words = sec.split()
        section_title = "Overview"
        first_line = sec.splitlines()[0].strip()
        if len(first_line) < 60 and not first_line.startswith("•") and not first_line.startswith("-"):
            section_title = first_line

        contextual_text = (
            f"Document: {doc_title} | Category: {category} | Section: {section_title}\n"
            f"{sec}"
        )
        chunk_id = f"{doc_id}_c{chunk_idx:02d}"
        chunks.append({
            "chunk_id": chunk_id,
            "doc_id": doc_id,
            "doc_title": doc_title,
            "category": category,
            "section_title": section_title,
            "source_file": file_path.name,
            "text": contextual_text,
            "raw_body": sec
        })
        chunk_idx += 1

    return chunks


# --- 3. Tokenizer for BM25 Sparse Keyword Search ---

def bm25_tokenize(text: str) -> List[str]:
    """Tokenizes text into lowercase alphanumeric terms for BM25 keyword matching."""
    text = text.lower()
    return re.findall(r'\b[a-z0-9_-]+\b', text)


# --- 4. Indexing Engine ---

class IndexPipeline:
    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self._embedder = None

    @property
    def embedder(self) -> SentenceTransformer:
        if self._embedder is None:
            print(f"[Indexer] Loading local CPU embedding model '{self.model_name}'...")
            t0 = time.perf_counter()
            self._embedder = SentenceTransformer(self.model_name, device="cpu")
            print(f"[Indexer] Model loaded in {(time.perf_counter() - t0):.2f}s")
        return self._embedder

    def run(self, force: bool = False, file_format: str = "md"):
        t_start = time.perf_counter()
        
        # Determine target documents directory and file pattern
        target_dir = DOCS_DIR
        pattern = "*.md"
        if file_format == "pdf":
            # Check pdf_documents folder first, then documents folder
            pdf_docs_dir = DATA_DIR / "pdf_documents"
            if pdf_docs_dir.exists() and list(pdf_docs_dir.glob("*.pdf")):
                target_dir = pdf_docs_dir
            pattern = "*.pdf"

        doc_files = sorted(list(target_dir.glob(pattern)))
        if not doc_files:
            print(f"[Indexer] Error: No {pattern} documents found in {target_dir}")
            return

        stored_hashes = load_stored_hashes()
        current_hashes = {f.name: compute_file_md5(f) for f in doc_files}

        # Check for changes
        added_files = [f for f in current_hashes if f not in stored_hashes]
        modified_files = [f for f in current_hashes if f in stored_hashes and current_hashes[f] != stored_hashes[f]]
        deleted_files = [f for f in stored_hashes if f not in current_hashes]

        needs_rebuild = force or bool(added_files or modified_files or deleted_files) or not CHUNKS_FILE.exists()

        if not needs_rebuild:
            print(f"[Indexer] All {len(doc_files)} documents ({pattern}) are up-to-date. (0 modified, 0 added). Index is fresh!")
            return

        print(f"[Indexer] Indexing required: {len(added_files)} added, {len(modified_files)} modified, {len(deleted_files)} removed (Force={force}, Format={file_format})")

        # Re-chunk all current documents
        all_chunks: List[Dict] = []
        for file_name in current_hashes:
            file_path = target_dir / file_name
            if file_path.suffix.lower() == ".pdf":
                file_chunks = chunk_pdf_document(file_path)
            else:
                file_chunks = chunk_markdown_document(file_path)
            all_chunks.extend(file_chunks)

        print(f"[Indexer] Created {len(all_chunks)} semantic chunks from {len(doc_files)} documents.")

        # Compute Dense Embeddings using all-MiniLM-L6-v2
        chunk_texts = [c["text"] for c in all_chunks]
        print(f"[Indexer] Computing dense embeddings for {len(chunk_texts)} chunks...")
        t_emb = time.perf_counter()
        embeddings = self.embedder.encode(
            chunk_texts,
            batch_size=32,
            show_progress_bar=True,
            normalize_embeddings=True  # L2 normalization for instant cosine similarity via dot-product
        )
        embeddings = np.array(embeddings, dtype=np.float32)
        print(f"[Indexer] Embeddings computed in {(time.perf_counter() - t_emb):.2f}s (Shape: {embeddings.shape})")

        # Build BM25 Sparse Index
        print(f"[Indexer] Building BM25 sparse keyword index...")
        tokenized_corpus = [bm25_tokenize(c["text"]) for c in all_chunks]
        bm25_index = BM25Okapi(tokenized_corpus)

        # Save artifacts to index directory
        with open(CHUNKS_FILE, "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, indent=2)

        np.save(EMBEDDINGS_FILE, embeddings)

        with open(BM25_FILE, "wb") as f:
            pickle.dump({
                "bm25": bm25_index,
                "corpus_size": len(all_chunks),
                "model_name": self.model_name
            }, f)

        save_stored_hashes(current_hashes)

        total_time = time.perf_counter() - t_start
        print(f"[Indexer] Indexing completed successfully in {total_time:.2f}s!")
        print(f"[Indexer] Chunks saved: {CHUNKS_FILE}")
        print(f"[Indexer] Dense matrix: {EMBEDDINGS_FILE}")
        print(f"[Indexer] BM25 model:  {BM25_FILE}")


def main():
    parser = argparse.ArgumentParser(description="Apex Car Rental Offline Indexer")
    parser.add_argument("--force", action="store_true", help="Force re-indexing of all documents from scratch")
    parser.add_argument("--format", choices=["md", "pdf"], default="md", help="Document format to index (md or pdf)")
    args = parser.parse_args()

    pipeline = IndexPipeline()
    pipeline.run(force=args.force, file_format=args.format)

if __name__ == "__main__":
    main()

