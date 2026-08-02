"""
工具定义模块

所有 Agent 可调用的工具函数都在这里定义。
使用 @tool 装饰器将普通 Python 函数注册为 LangChain 工具，
Agent 会在需要时自动调用这些工具来获取信息或执行操作。

扩展方式：添加新的 @tool 函数，然后在 agent.py 中注册即可。
"""
import os
import requests
from langchain.tools import tool


# ==================== 天气查询工具 ====================

@tool
def getWeather(location: str) -> str:
    """
    查询指定城市的实时天气。调用 Open-Meteo 免费天气 API 获取真实数据。

    Args:
        location: 城市名称（如 "北京"）或英文城市名（如 "Beijing"）

    Returns:
        该城市的天气描述字符串（温度、风速、天气状况）
    """
    # 城市经纬度映射（Open-Meteo 需要坐标查询）
    city_coords = {
        "北京": (39.9042, 116.4074),
        "beijing": (39.9042, 116.4074),
        "上海": (31.2304, 121.4737),
        "shanghai": (31.2304, 121.4737),
        "杭州": (30.2741, 120.1551),
        "hangzhou": (30.2741, 120.1551),
        "深圳": (22.5431, 114.0579),
        "shenzhen": (22.5431, 114.0579),
        "广州": (23.1291, 113.2644),
        "guangzhou": (23.1291, 113.2644),
        "成都": (30.5728, 104.0668),
        "chengdu": (30.5728, 104.0668),
    }

    coords = city_coords.get(location.lower() if isinstance(location, str) else location)
    if not coords:
        return f"暂不支持查询 {location} 的天气，请尝试英文名称或更换城市"

    lat, lon = coords
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,wind_speed_10m,weather_code"
        f"&timezone=auto"
    )

    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        current = data["current"]
        temp = current["temperature_2m"]
        wind = current["wind_speed_10m"]

        # 简单天气码映射
        weather_map = {0: "晴天", 1: "少云", 2: "多云", 3: "阴天", 45: "雾",
                       51: "小雨", 61: "中雨", 71: "小雪", 80: "阵雨", 95: "雷阵雨"}
        weather_code = current.get("weather_code", 0)
        weather_desc = weather_map.get(weather_code, "未知")

        return f"{location}当前天气：{weather_desc}，温度 {temp}°C，风速 {wind} km/h"
    except Exception as e:
        return f"获取 {location} 天气失败: {str(e)}"


# ==================== Tavily 搜索工具 ====================

@tool
def webSearch(query: str) -> str:
    """
    使用 Tavily 搜索引擎搜索互联网实时信息。
    当需要查询最新资讯、新闻、事实性知识时使用。

    Args:
        query: 搜索关键词

    Returns:
        搜索结果摘要
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "错误：未配置 TAVILY_API_KEY，请检查 .env 文件"

    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "max_results": 3,
    }

    try:
        resp = requests.post(url, json=payload, timeout=15)
        data = resp.json()

        results = data.get("results", [])
        if not results:
            return f"未搜索到与 '{query}' 相关的结果"

        lines = [f"搜索结果 for '{query}':"]
        for r in results:
            lines.append(f"- {r['title']}: {r['content'][:200]}...")
        return "\n".join(lines)
    except Exception as e:
        return f"搜索失败: {str(e)}"
