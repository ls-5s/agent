"""Agent 工具：知识库检索 + 联网搜索"""
from langchain.tools import tool
from vector_store import search


@tool
def knowledge_base_search(query: str) -> str:
    """检索本地知识库中的文档内容。当用户询问个人笔记、上传的文档、学习资料等私有知识时使用此工具。
    Args:
        query: 搜索查询语句
    """
    docs = search(query, k=4)
    if not docs:
        return "知识库中未找到相关内容。"

    results = []
    for i, doc in enumerate(docs, 1):
        src = doc.metadata.get("source", "unknown")
        results.append(f"[{i}] 来源: {src}\n{doc.page_content}")
    return "\n\n".join(results)


@tool
def web_search(query: str) -> str:
    """联网搜索实时信息。当用户询问新闻、最新技术、外部知识等本地知识库无法回答的问题时使用此工具。
    Args:
        query: 搜索查询语句
    """
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        return "联网搜索不可用（缺少 duckduckgo-search 包）。"

    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=5):
                results.append(f"- {r['title']}\n  {r['body']}\n  链接: {r['href']}")
        return "\n\n".join(results) if results else "未找到相关网络结果。"
    except Exception as e:
        return f"联网搜索失败: {e}"
