"""
Agent 模块

负责创建和配置智能体。使用 LangChain 推荐的 init_chat_model 统一初始化模型。
提供两种输出模式：
1. create_weather_agent() — 普通 Agent，自由文本回复
2. format_structured_answer() — 提示词约束 + Pydantic 解析，返回结构化 AnswerInfo
"""
import json
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from config import MODEL_NAME
from tools import getWeather, webSearch
from schemas import AnswerInfo


def create_weather_agent():
    """
    创建天气助手 Agent（自由文本模式）。

    Returns:
        配置完成的 LangChain Agent 实例
    """
    llm = init_chat_model(MODEL_NAME)
    return create_agent(
        llm,
        tools=[getWeather, webSearch]
    )


def format_structured_answer(user_question: str, tool_results: list[str]) -> AnswerInfo:
    """
    用提示词约束 + Pydantic 解析，将 Agent 结果转为结构化输出。

    方案：通过 SystemMessage 要求模型输出严格 JSON 格式，
    然后手动解析为 AnswerInfo 对象，兼容不支持原生 structured_output 的模型。

    Args:
        user_question: 用户原始问题
        tool_results: Agent 工具调用结果列表

    Returns:
        AnswerInfo 对象（answer + reference 列表）
    """
    llm = init_chat_model(MODEL_NAME)

    # 用提示词强制模型输出 JSON
    system_prompt = (
        "你是一个结果格式化助手。请根据工具返回的数据，输出严格 JSON。\n\n"
        "输出格式（不要输出任何其他文字，只输出 JSON）：\n"
        '{\n'
        '  "answer": "最终回答（中文）",\n'
        '  "reference": [\n'
        '    {"title": "来源标题", "url": "来源链接"}\n'
        '  ]\n'
        '}\n\n'
        "要求：\n"
        "1. answer 字段用中文，简洁直白\n"
        "2. reference 数组列出所有引用的来源，title 和 url 从工具结果中提取\n"
        "3. 输出必须是合法的 JSON，不要有多余文字"
    )

    context = (
        f"用户问题：{user_question}\n\n"
        f"工具返回数据：\n" + "\n---\n".join(tool_results)
    )

    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": context},
    ])

    raw = response.content.strip()

    # 清理可能的 markdown 代码块包裹
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        if raw.endswith("```"):
            raw = raw[:-3]

    return AnswerInfo.model_validate_json(raw)
