"""
data/chroma_loader.py
Loads Excel questionnaire files (CLIENT/AREA/QUESTION/ANSWER) from backend/files/
into a persistent ChromaDB vector store.

Run directly to build or rebuild the store:
    python data/chroma_loader.py
"""
from __future__ import annotations

# Fix for older SQLite3 on Linux (ChromaDB requires >= 3.35.0)
__import__("pysqlite3")
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from pathlib import Path
import openpyxl
import chromadb
from chromadb.utils import embedding_functions

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR       = Path(__file__).parent.parent
FILES_DIR      = BASE_DIR / "files"
CHROMA_DIR     = BASE_DIR / "chroma_db"
COLLECTION_NAME = "hla_questions"

# ── Excel filename → HCM module name ─────────────────────────────────────────
FILENAME_TO_MODULE: dict[str, str] = {
    "Absence":           "Workforce Management",
    "Compensation":      "Compensation & Benefits",
    "Global_HR":         "Core HR",
    "Payroll":           "Payroll",
    "Recruiting":        "Talent Management",
    "Talent_Management": "Talent Management",
}


def _read_excel_rows() -> list[dict]:
    """Read every .xlsx file in FILES_DIR and return normalised question records."""
    records: list[dict] = []
    for xlsx_path in sorted(FILES_DIR.glob("*.xlsx")):
        stem   = xlsx_path.stem
        module = FILENAME_TO_MODULE.get(stem, stem.replace("_", " "))
        wb     = openpyxl.load_workbook(xlsx_path, data_only=True)
        ws     = wb.active
        for row in ws.iter_rows(min_row=2, values_only=True):
            client   = str(row[0] or "").strip()
            area     = str(row[1] or "").strip()
            question = str(row[2] or "").strip()
            answer   = str(row[3] or "").strip()
            if not question:
                continue
            records.append({
                "module":   module,
                "client":   client,
                "area":     area,
                "question": question,
                "answer":   answer,
            })
    return records


def _get_chroma_client() -> chromadb.ClientAPI:
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def build_vector_store(force_rebuild: bool = False) -> chromadb.Collection:
    """
    Create (or load) the ChromaDB collection.

    If force_rebuild=True the existing collection is deleted and rebuilt from
    the Excel files currently present in FILES_DIR.
    """
    client = _get_chroma_client()
    ef     = embedding_functions.DefaultEmbeddingFunction()

    existing_names = [c.name for c in client.list_collections()]

    if COLLECTION_NAME in existing_names and not force_rebuild:
        return client.get_collection(name=COLLECTION_NAME, embedding_function=ef)

    if COLLECTION_NAME in existing_names:
        client.delete_collection(COLLECTION_NAME)

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )

    records = _read_excel_rows()
    if not records:
        print(f"WARNING: No rows found in {FILES_DIR}")
        return collection

    ids       = [f"q_{i}" for i in range(len(records))]
    # Embed the question text; area prefix gives semantic context
    documents = [f"{r['area']}: {r['question']}" for r in records]
    metadatas = [
        {
            "module":   r["module"],
            "area":     r["area"],
            "client":   r["client"],
            "question": r["question"],
            "answer":   r["answer"],
        }
        for r in records
    ]

    collection.add(ids=ids, documents=documents, metadatas=metadatas)
    print(f"ChromaDB: loaded {len(records)} questions from {FILES_DIR}")
    return collection


if __name__ == "__main__":
    build_vector_store(force_rebuild=True)
    print("Done.")
