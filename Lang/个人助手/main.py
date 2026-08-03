"""FastAPI 接口服务 — 个人知识库智能助手"""
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
from typing import List

from config import UPLOAD_DIR, BASE_DIR
from document_loader import load_and_split
from vector_store import add_documents, clear, get_stats
from rag_chain import ask_rag, ask_rag_stream
from agent import ask_agent, ask_agent_stream

app = FastAPI(title="个人知识库智能助手", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str
    sources: List[str] = []


class StatusResponse(BaseModel):
    total_documents: int
    upload_dir: str


@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """上传文档（PDF / TXT / MD），自动分片并构建向量知识库"""
    uploaded = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        try:
            docs = load_and_split(file_path)
            count = add_documents(docs)
            uploaded.append({"filename": file.filename, "chunks": count})
        except ValueError as e:
            raise HTTPException(400, str(e))
        except Exception as e:
            raise HTTPException(500, f"处理 {file.filename} 失败: {e}")

    return {"message": f"成功上传 {len(uploaded)} 个文件", "details": uploaded}


@app.post("/ask/rag")
async def ask_rag_endpoint(req: QuestionRequest):
    """纯 RAG 问答：仅检索本地知识库生成回答"""
    return ask_rag(req.question)


@app.post("/ask/rag/stream")
async def ask_rag_stream_endpoint(req: QuestionRequest):
    """纯 RAG 问答（流式）：逐字返回"""
    return StreamingResponse(
        ask_rag_stream(req.question),
        media_type="text/event-stream",
    )


@app.post("/ask/agent")
async def ask_agent_endpoint(req: QuestionRequest):
    """Agent 智能问答：自动判断走知识库检索或联网搜索"""
    return ask_agent(req.question)


@app.post("/ask/agent/stream")
async def ask_agent_stream_endpoint(req: QuestionRequest):
    """Agent 智能问答（流式）：逐字返回"""
    return StreamingResponse(
        ask_agent_stream(req.question),
        media_type="text/event-stream",
    )


@app.delete("/knowledge-base")
async def clear_knowledge_base():
    """清空知识库"""
    clear()
    return {"message": "知识库已清空"}


@app.get("/")
async def index():
    html_path = os.path.join(BASE_DIR, "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.get("/status")
async def status():
    """查询知识库状态"""
    stats = get_stats()
    return StatusResponse(
        total_documents=stats["total_documents"],
        upload_dir=UPLOAD_DIR,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
