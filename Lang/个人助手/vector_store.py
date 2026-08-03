"""Chroma 向量库操作"""
import os
import shutil
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import VECTOR_DB_DIR, EMBEDDING_MODEL, TOP_K

_vector_store = None


def _get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def get_vector_store():
    global _vector_store
    if _vector_store is None:
        _vector_store = Chroma(
            persist_directory=VECTOR_DB_DIR,
            embedding_function=_get_embeddings(),
        )
    return _vector_store


def add_documents(docs):
    vs = get_vector_store()
    vs.add_documents(docs)
    return len(docs)


def search(query: str, k: int = TOP_K):
    vs = get_vector_store()
    return vs.similarity_search(query, k=k)


def clear():
    global _vector_store
    _vector_store = None
    if os.path.exists(VECTOR_DB_DIR):
        shutil.rmtree(VECTOR_DB_DIR)
        os.makedirs(VECTOR_DB_DIR)


def get_stats():
    try:
        vs = get_vector_store()
        count = vs._collection.count()
    except Exception:
        count = 0
    return {"total_documents": count}
