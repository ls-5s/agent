"""
Agent 模块

负责创建和配置智能体。使用 LangChain 推荐的 init_chat_model 统一初始化模型，
让 main.py 只需调用 create_weather_agent() 即可获取一个可用的 Agent。
"""
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from config import MODEL_NAME
from tools import getWeather, webSearch


def create_weather_agent():
    """
    创建天气助手 Agent。

    使用 init_chat_model（LangChain 推荐的统一工厂函数）自动识别模型厂商，
    绑定天气查询和网页搜索两个工具，返回可直接调用的 Agent 实例。

    Returns:
        配置完成的 LangChain Agent 实例
    """
    llm = init_chat_model(MODEL_NAME)
    return create_agent(
        llm,
        tools=[getWeather, webSearch]
    )
