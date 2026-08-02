"""
Agent 模块

负责创建和配置智能体。使用 ChatOpenAI 兼容接口对接 DeepSeek，
让 main.py 只需调用 create_weather_agent() 即可获取一个可用的 Agent。
"""
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from config import MODEL_NAME, OPENAI_API_KEY, OPENAI_BASE_URL
from tools import getWeather, webSearch


def create_weather_agent():
    """
    创建天气助手 Agent。

    通过 ChatOpenAI（兼容接口）对接 DeepSeek 模型，
    绑定天气查询和网页搜索两个工具，返回可直接调用的 Agent 实例。
    Agent 会自动处理：理解用户意图 → 判断是否需要调用工具 →
    调用工具获取数据 → 根据工具返回结果生成最终回复。

    Returns:
        配置完成的 LangChain Agent 实例
    """
    llm = ChatOpenAI(
        model=MODEL_NAME,
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
    )
    return create_agent(
        llm,
        tools=[getWeather, webSearch]
    )
