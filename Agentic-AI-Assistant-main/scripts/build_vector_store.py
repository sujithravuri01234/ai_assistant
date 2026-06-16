"""
build_vector_store.py
---------------------
Loads all QA datasets from the /data folder and indexes them into
a local ChromaDB vector store with department-level metadata.
Uses sentence-transformers for local embeddings (no API key needed).
"""

import os
import json
import glob
from pathlib import Path
from dotenv import load_dotenv
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings

load_dotenv()

# ─── Config ──────────────────────────────────────────────────────────────────
COLLECTION_NAME = "sujith_knowledge_base"

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"

# ─── Local Embedding Function (sentence-transformers, no API needed) ──────────

# We will use chromadb's built-in ONNX embedding function, no class definition needed here.


def load_all_qa_data():
    """Load all JSON QA files from the data directory."""
    all_qa = []
    json_files = glob.glob(str(DATA_DIR / "*.json"))
    for file_path in json_files:
        with open(file_path, "r", encoding="utf-8") as f:
            qa_list = json.load(f)
            all_qa.extend(qa_list)
    print(f"[OK] Loaded {len(all_qa)} QA pairs from {len(json_files)} departments.")
    return all_qa


def build_vector_store():
    """Embed QA pairs and store in ChromaDB with metadata."""
    print("\n[*] Building Sujith Vector Store ...\n")

    # Initialize ChromaDB client
    VECTOR_STORE_DIR.mkdir(exist_ok=True)
    client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))

    # Use ChromaDB's built-in ONNX embedding function
    from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2
    print("[*] Loading embedding model: all-MiniLM-L6-v2 (ONNX local, lightweight)")
    ef = ONNXMiniLM_L6_V2()

    # Delete and recreate collection for fresh build
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"[*] Cleared existing collection: {COLLECTION_NAME}")
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"}
    )

    # Load all QA data
    qa_data = load_all_qa_data()

    # Prepare documents, metadatas, and ids
    documents = []
    metadatas = []
    ids = []

    for i, qa in enumerate(qa_data):
        doc_text = f"Question: {qa['question']}\nAnswer: {qa['answer']}"
        documents.append(doc_text)
        metadatas.append({
            "department": qa["department"],
            "audience": qa["audience"],
            "question": qa["question"],
            "answer": qa["answer"]
        })
        ids.append(f"doc_{i:04d}")

    # Add to collection in batches
    batch_size = 10
    for start in range(0, len(documents), batch_size):
        end = min(start + batch_size, len(documents))
        collection.add(
            documents=documents[start:end],
            metadatas=metadatas[start:end],
            ids=ids[start:end]
        )
        print(f"   -> Indexed documents {start} - {end}")

    print(f"\n[DONE] Vector store built successfully!")
    print(f"   Collection: '{COLLECTION_NAME}'")
    print(f"   Total documents: {collection.count()}")
    print(f"   Stored at: {VECTOR_STORE_DIR}\n")

    return collection


if __name__ == "__main__":
    build_vector_store()
