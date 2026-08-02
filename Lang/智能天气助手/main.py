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
                {"role": "user", "content": user_input}
            ]
        })

        # 展示每一步过程：模型思考 → 工具调用 → 工具结果 → 最终回复
        step = 0
        for msg in response["messages"]:
            if not hasattr(msg, "content") or not msg.content:
                continue

            content = msg.content.encode("gbk", errors="ignore").decode("gbk")

            if msg.type == "human":
                print(f"[步骤{step}] 用户输入")
                print(f"  {content}\n")
                step += 1
            elif msg.type == "ai":
                print(f"[步骤{step}] 模型回复")
                print(f"  {content}\n")
                step += 1
            elif msg.type == "tool":
                print(f"[步骤{step}] 工具调用结果")
                print(f"  {content}\n")
                step += 1

        print("─" * 50)


# 仅当直接运行此文件时执行 main()，被 import 时不执行
if __name__ == "__main__":
    main()
