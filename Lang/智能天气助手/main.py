"""
程序入口

智能天气助手的主流程：
1. Agent 执行工具调用（展示 ReAct 过程）
2. 结构化 LLM 格式化最终回复（Pydantic 输出，含引用来源）
3. 展示两部分结果

运行方式：
    python main.py
"""
from langchain_core.messages import SystemMessage, HumanMessage
from agent import create_weather_agent, format_structured_answer


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

        # ====== 第一阶段：Agent 执行工具调用 ======
        print("=" * 50)
        print("[Agent 阶段] ReAct 工具调用过程")

        response = agent.invoke({
            "messages": [
                SystemMessage(content="你是专业天气预报助手，回答简洁直白，用中文回复。"),
                HumanMessage(content=user_input),
            ]
        })

        # 收集工具调用结果（用于后续结构化输出）
        tool_results = []
        step = 0
        type_map = {
            "system": "SystemMessage（系统设定）",
            "human":  "HumanMessage（用户输入）",
            "ai":     "AIMessage（模型回复/工具调用指令）",
            "tool":   "ToolMessage（工具执行结果）",
        }

        for msg in response["messages"]:
            # AI 消息：可能只有 tool_calls 没有 content
            if msg.type == "ai" and hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    print(f"[步骤{step}] AIMessage（工具调用指令）")
                    print(f"  调用工具: {tc['name']}({tc['args']})")
                    step += 1
                if not msg.content:
                    continue

            if not hasattr(msg, "content") or not msg.content:
                continue

            content = msg.content.encode("gbk", errors="ignore").decode("gbk")
            label = type_map.get(msg.type, msg.type)
            print(f"[步骤{step}] {label}")
            print(f"  {content[:150]}{'...' if len(content) > 150 else ''}")
            step += 1

            # 收集工具结果
            if msg.type == "tool":
                tool_results.append(content)

        # ====== 第二阶段：结构化输出 ======
        print("\n[结构化阶段] Pydantic AnswerInfo 对象")
        try:
            result = format_structured_answer(user_input, tool_results)
            print(f"  answer: {result.answer}")
            if result.reference:
                print(f"  reference ({len(result.reference)} 条):")
                for ref in result.reference:
                    print(f"    title: {ref.title}")
                    print(f"    url:   {ref.url}")
        except Exception as e:
            print(f"  解析失败: {e}")

        print()


if __name__ == "__main__":
    main()
