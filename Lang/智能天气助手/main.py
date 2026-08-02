"""
程序入口

智能天气助手的主流程：
1. 创建 Agent（自动加载配置和工具）
2. 用 SystemMessage 设定角色 + HumanMessage 接收用户输入
3. 展示完整的 ReAct 消息流转过程

运行方式：
    python main.py
"""
from langchain_core.messages import SystemMessage, HumanMessage
from agent import create_weather_agent


def main():
    agent = create_weather_agent()
    print("智能天气助手已启动！（输入 quit 退出）\n")

    while True:
        user_input = input(">>> 请输入问题: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("已退出。")
            break

        print("正在处理...\n")
        response = agent.invoke({
            "messages": [
                SystemMessage(content="你是专业天气预报助手，回答简洁直白，用中文回复。"),
                HumanMessage(content=user_input),
            ]
        })

        # 展示消息流转过程：SystemMessage → HumanMessage → AIMessage → ToolMessage
        step = 0
        type_map = {
            "system": "SystemMessage（系统设定）",
            "human":  "HumanMessage（用户输入）",
            "ai":     "AIMessage（模型回复/工具调用指令）",
            "tool":   "ToolMessage（工具执行结果）",
        }

        for msg in response["messages"]:
            if not hasattr(msg, "content") or not msg.content:
                # AIMessage 可能只有 tool_calls 没有 content
                if msg.type == "ai" and hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tc in msg.tool_calls:
                        label = type_map.get(msg.type, msg.type)
                        print(f"[步骤{step}] {label}")
                        print(f"  调用工具: {tc['name']}({tc['args']})\n")
                        step += 1
                continue

            content = msg.content.encode("gbk", errors="ignore").decode("gbk")
            label = type_map.get(msg.type, msg.type)
            print(f"[步骤{step}] {label}")
            print(f"  {content}\n")
            step += 1

        print("─" * 50)


# 仅当直接运行此文件时执行 main()，被 import 时不执行
if __name__ == "__main__":
    main()
