"""
程序入口

智能天气助手的主流程：
1. 创建 Agent（自动加载配置和工具）
2. 发送用户消息
3. 处理并展示 Agent 的回复

运行方式：
    python main.py
"""
from agent import create_weather_agent


def main():
    # 获取配置好的天气助手 Agent
    agent = create_weather_agent()

    # 发送用户问题，Agent 会自动判断是否需要调用 getWeather 工具
    print(">>> 正在调用大模型...")
    response = agent.invoke({
        "messages": [
            {"role": "user", "content": "杭州今天天气如何?"}
        ]
    })

    # 遍历 Agent 返回的消息列表
    # - HumanMessage：用户输入
    # - AIMessage：模型回复
    # - ToolMessage：工具调用结果
    for msg in response["messages"]:
        if hasattr(msg, "content"):
            # 忽略特殊字符，避免 Windows GBK 终端编码报错
            content = msg.content.encode("gbk", errors="ignore").decode("gbk")
            print(f"\n[{msg.type}] {content}")


# 仅当直接运行此文件时执行 main()，被 import 时不执行
if __name__ == "__main__":
    main()
