"""
data/question_store.py
Retrieval layer over the ChromaDB question store.

Provides:
  get_questions_by_module(module, n)  – all (or top-n) questions for a module
  search_questions(query, module, n)  – semantic search with optional module filter
  rebuild_store()                     – force rebuild from Excel files
"""
from __future__ import annotations

# Fix for older SQLite3 on Linux (ChromaDB requires >= 3.35.0)
__import__("pysqlite3")
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from functools import lru_cache
import chromadb
from chromadb.utils import embedding_functions
from data.chroma_loader import (
    build_vector_store,
    COLLECTION_NAME,
    CHROMA_DIR,
)


@lru_cache(maxsize=1)
def _collection() -> chromadb.Collection:
    """Lazily load (and cache) the ChromaDB collection."""
    return build_vector_store(force_rebuild=False)


def _row_to_question(meta: dict) -> dict:
    """Convert a ChromaDB metadata dict to the format expected by excel_service."""
    return {
        "category": meta.get("area", ""),
        "question": meta.get("question", ""),
        "priority": "Medium",
        "guidance": meta.get("answer", ""),
    }


def get_questions_by_module(module: str, n: int = 0) -> list[dict]:
    """
    Return questions for the given HCM module name.

    n=0 (default) returns every matching question.
    Positive n returns at most n questions (semantic top-n via query).
    """
    coll = _collection()

    if n == 0:
        result = coll.get(
            where={"module": module},
            include=["metadatas"],
        )
        return [_row_to_question(m) for m in result["metadatas"]]

    # Semantic top-n: query with module name as the search context
    total = coll.count()
    if total == 0:
        return []

    result = coll.query(
        query_texts=[module],
        n_results=min(n, total),
        where={"module": module},
        include=["metadatas"],
    )
    return [_row_to_question(m) for m in result["metadatas"][0]]


def search_questions(query: str, module: str = "", n: int = 20) -> list[dict]:
    """
    Semantic search across all questions, optionally limited to one module.
    Useful for ad-hoc retrieval (e.g. "payroll compliance requirements").
    """
    coll  = _collection()
    total = coll.count()
    if total == 0:
        return []

    kwargs: dict = {
        "query_texts": [query],
        "n_results":   min(n, total),
        "include":     ["metadatas"],
    }
    if module:
        kwargs["where"] = {"module": module}

    result = coll.query(**kwargs)
    return [_row_to_question(m) for m in result["metadatas"][0]]


def rebuild_store() -> int:
    """Rebuild ChromaDB from Excel files and return number of documents loaded."""
    _collection.cache_clear()
    coll = build_vector_store(force_rebuild=True)
    _collection.cache_clear()  # ensure next call re-fetches rebuilt collection
    return coll.count()
