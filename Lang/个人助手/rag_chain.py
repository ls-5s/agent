"""RAG 检索增强生成"""
import json
from langchain.chat_models import init_chat_model
from config import LLM_MODEL, LLM_API_KEY, LLM_BASE_URL, LLM_TEMPERATURE, TOP_K
from vector_store import search


def _get_llm():
    return init_chat_model(
        LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        api_key=LLM_API_KEY,
        base_url=LLM_BASE_URL,
    )


def ask_rag(question: str) -> dict:
    """检索本地知识库并生成回答"""
    docs = search(question, k=TOP_K)
    sources = [doc.metadata.get("source", "unknown") for doc in docs]

    if not docs:
        return {
            "answer": "知识库中暂无相关内容，请先上传文档或使用 /ask/agent 进行联网搜索。",
            "sources": [],
        }

    context_parts = [f"[{i}] {doc.page_content}" for i, doc in enumerate(docs, 1)]
    context = "\n\n".join(context_parts)

    llm = _get_llm()
    prompt = f"""你是一个个人知识库助手。请基于以下检索到的文档内容回答问题。
如果文档内容不足以回答问题，请明确说明，不要编造信息。
回答时请引用来源编号。

## 文档内容
{context}

## 用户问题
{question}

## 回答"""
    response = llm.invoke(prompt)
    return {"answer": response.content, "sources": sources}


def ask_rag_stream(question: str):
    """检索本地知识库并流式生成回答（SSE 格式）"""
    docs = search(question, k=TOP_K)
    sources = [doc.metadata.get("source", "unknown") for doc in docs]

    yield f"data: {json.dumps({'type': 'sources', 'data': sources})}\n\n"

    if not docs:
        yield f"data: {json.dumps({'type': 'text', 'data': '知识库中暂无相关内容，请先上传文档或使用 /ask/agent 进行联网搜索。'})}\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
        return

    context_parts = [f"[{i}] {doc.page_content}" for i, doc in enumerate(docs, 1)]
    context = "\n\n".join(context_parts)

    llm = _get_llm()
    prompt = f"""你是一个个人知识库助手。请基于以下检索到的文档内容回答问题。
如果文档内容不足以回答问题，请明确说明，不要编造信息。
回答时请引用来源编号。

## 文档内容
{context}

## 用户问题
{question}

## 回答"""
    for chunk in llm.stream(prompt):
        if chunk.content:
            yield f"data: {json.dumps({'type': 'text', 'data': chunk.content})}\n\n"

    yield f"data: {json.dumps({'type': 'done'})}\n\n"
