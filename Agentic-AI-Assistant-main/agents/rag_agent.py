"""
rag_agent.py
------------
Retrieves relevant context from ChromaDB and generates an answer using a
waterfall AI cascade:
  1) Context-grounded answer (strict)
  2) General company-support answer (fallback)
  3) Broader helpful assistant answer (final fallback)
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv(override=True)

COLLECTION_NAME = "sujith_knowledge_base"
TOP_K = int(os.getenv("RAG_TOP_K", "3"))
BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_STORE_DIR = BASE_DIR / "vector_store"


_chroma_client = None
_collection = None


def _get_collection():
    global _chroma_client, _collection
    if _collection is None:
        from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2
        ef = ONNXMiniLM_L6_V2()
        _chroma_client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
        _collection = _chroma_client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=ef,
        )
    return _collection


def _resolve_models() -> list[str]:
    """Get 2-3 cascade models from env, with sane defaults."""
    raw = os.getenv(
        "GROQ_CASCADE_MODELS",
        "llama-3.3-70b-versatile,llama-3.1-8b-instant,mixtral-8x7b-32768",
    )
    models = [m.strip() for m in raw.split(",") if m.strip()]
    return models[:3] if models else ["llama-3.3-70b-versatile"]


def _invoke_with_fallback(prompt: ChatPromptTemplate, payload: dict, temperature: float = 0.25) -> str:
    """
    Waterfall model invocation:
    Try model-1 -> model-2 -> model-3 until one succeeds.
    """
    api_key = os.getenv("GROQ_API_KEY")
    last_error = None

    for model_name in _resolve_models():
        try:
            llm = ChatGroq(model=model_name, api_key=api_key, temperature=temperature)
            chain = prompt | llm
            result = chain.invoke(payload)
            content = (result.content or "").strip()
            if content:
                return content
        except Exception as err:
            last_error = err
            continue

    if last_error:
        raise last_error
    raise RuntimeError("All cascade models returned empty output.")


RAG_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful AI assistant for Sujith, a retail company.
Use ONLY the context provided below to answer the user's question.
If the context does not contain the answer, reply exactly with: CONTEXT_NOT_SUFFICIENT

Context from Sujith Knowledge Base:
{context}
""",
        ),
        ("human", "{query}"),
    ]
)

GENERAL_SUPPORT_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are Sujith's AI support assistant.
The internal KB did not have a direct match, so provide a practical, generally helpful answer.
Rules:
- Do not claim you checked logs or files.
- Be transparent that this is best-effort guidance.
- Give clear next steps.
- Keep tone concise and helpful.
- If question needs account-specific/internal data, ask user to share details or contact support.
""",
        ),
        ("human", "Department hint: {department}\nUser question: {query}"),
    ]
)

FINAL_FALLBACK_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a reliable general AI assistant.
Provide a safe, actionable response when internal knowledge is unavailable.
Keep it short, structured, and user-friendly.
""",
        ),
        ("human", "{query}"),
    ]
)


def _build_context(metadatas: list[dict]) -> str:
    context_parts = []
    for meta in metadatas:
        context_parts.append(f"Q: {meta.get('question', '')}\nA: {meta.get('answer', '')}")
    return "\n\n---\n\n".join(context_parts)


def _query_collection(query: str, department: str) -> tuple[list[str], list[dict]]:
    collection = _get_collection()

    if department and department != "unknown":
        results = collection.query(
            query_texts=[query],
            n_results=TOP_K,
            where={"department": department},
        )
        docs = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        if docs:
            return docs, metadatas

    # Fallback retrieval across all departments.
    results = collection.query(query_texts=[query], n_results=TOP_K)
    docs = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    return docs, metadatas


def retrieve_and_answer(query: str, department: str) -> str:
    """
    Main retrieval + AI waterfall cascade.
    """
    docs, metadatas = _query_collection(query, department)

    if docs and metadatas:
        context = _build_context(metadatas)
        rag_answer = _invoke_with_fallback(RAG_PROMPT, {"context": context, "query": query}, temperature=0.2)
        if rag_answer.strip() != "CONTEXT_NOT_SUFFICIENT":
            return rag_answer

    # Stage 2: department-aware general answer
    try:
        return _invoke_with_fallback(
            GENERAL_SUPPORT_PROMPT,
            {"department": department or "unknown", "query": query},
            temperature=0.35,
        )
    except Exception:
        pass

    # Stage 3: final broad fallback
    return _invoke_with_fallback(FINAL_FALLBACK_PROMPT, {"query": query}, temperature=0.4)


if __name__ == "__main__":
    samples = [
        ("How many leave days do I get?", "HR"),
        ("How do I reset my company email password?", "IT Support"),
        ("What is your return policy?", "Customer Support"),
        ("Is there any discount on electronics today?", "Product & Promotions"),
        ("Can you suggest a way to write a complaint email?", "unknown"),
    ]
    for query, dept in samples:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"Department: {dept}")
        print(f"Answer:\n{retrieve_and_answer(query, dept)}")
