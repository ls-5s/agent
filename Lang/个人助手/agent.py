"""ReAct Agent：智能路由知识库 / 联网搜索"""
import json
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage
from config import LLM_MODEL, LLM_API_KEY, LLM_BASE_URL, LLM_TEMPERATURE
from tools import knowledge_base_search, web_search

_agent = None
_checkpointer = None


def _get_agent():
    global _agent, _checkpointer
    if _agent is None:
        llm = init_chat_model(
            LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            api_key=LLM_API_KEY,
            base_url=LLM_BASE_URL,
        )

        system_prompt = """你是一个个人知识库智能助手，具备以下两种工具：

- knowledge_base_search: 检索本地私有文档（笔记、PDF、技术文档等）
- web_search: 联网搜索实时信息

决策规则：
1. 用户询问个人文档、笔记、已上传资料 → 使用 knowledge_base_search
2. 用户询问新闻、最新技术、实时信息等知识库无法覆盖的内容 → 使用 web_search
3. 必要时可同时使用两个工具，综合多源信息后给出答案
4. 回答时引用信息来源"""

        _checkpointer = InMemorySaver()
        _agent = create_agent(
            model=llm,
            tools=[knowledge_base_search, web_search],
            system_prompt=system_prompt,
            checkpointer=_checkpointer,
        )
    return _agent, _checkpointer


def ask_agent(question: str) -> dict:
    agent, checkpointer = _get_agent()
    config = {"configurable": {"thread_id": "default"}}

    result = agent.invoke(
        {"messages": [HumanMessage(content=question)]},
        config=config,
    )
    answer = result["messages"][-1].content
    return {"answer": answer, "sources": []}


def ask_agent_stream(question: str):
    """Agent 流式问答，用 SSE 格式逐字输出最终答案"""
    agent, checkpointer = _get_agent()
    config = {"configurable": {"thread_id": "default"}}

    # 先收集完整回答，再逐字输出（Agent 内部多步推理不适合逐 token 流式）
    result = agent.invoke(
        {"messages": [HumanMessage(content=question)]},
        config=config,
    )
    answer = result["messages"][-1].content

    # 模拟逐字输出
    for ch in answer:
        yield f"data: {json.dumps({'type': 'text', 'data': ch})}\n\n"

    yield f"data: {json.dumps({'type': 'done'})}\n\n"
