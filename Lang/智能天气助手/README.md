# 智能天气助手

LangChain Agent 实战项目，基于 DeepSeek 模型的智能天气助手，支持天气查询和网页搜索。

## 功能

| 工具 | 说明 |
|------|------|
| `getWeather` | 调用 Open-Meteo 免费 API，查询城市实时天气（温度、风速、天气状况） |
| `webSearch` | 调用 Tavily 搜索引擎，检索互联网实时信息 |

## 项目结构

```
智能天气助手/
├── .env           # 环境变量（API Key），不提交 Git
├── config.py      # 配置管理，统一加载 .env
├── tools.py       # 工具定义（getWeather / webSearch）
├── agent.py       # Agent 创建（ChatOpenAI + create_agent）
├── main.py        # 交互式入口
└── README.md      # 本文件
```

## 快速开始

### 1. 安装依赖

```bash
pip install langchain langchain-openai python-dotenv requests
```

### 2. 配置 .env

```bash
OPENAI_API_KEY=sk-your-key
OPENAI_BASE_URL=https://api.deepseek.com/v1
MODEL_NAME=deepseek-v4-pro
TAVILY_API_KEY=tvly-your-key
```

### 3. 运行

```bash
python main.py
```

```
智能天气助手已启动！（输入 quit 退出）

>>> 请输入问题: 北京今天天气怎么样？
正在处理...

[步骤1] 模型思考 → [步骤2] 工具调用结果 → [步骤3] 最终回复: 北京晴天 25°C
```

输入 `quit` / `exit` / `q` 退出。

## Agent 工作流程

```
用户输入 → 模型思考 → 需要工具？→ 调用工具 → 获取结果 → 综合输出
                ↑                              |
                └──── 可能多轮循环 ─────────────┘
```

运行时会展示每一步过程，可看到 Agent 完整的思考-行动循环。

## langchain 技术栈

| 语法 | 用途 |
|------|------|
| `ChatOpenAI` | OpenAI 兼容接口对接 DeepSeek |
| `@tool` | 将 Python 函数注册为 Agent 工具 |
| `create_agent` | 一键创建 ReAct Agent |

## 相关链接

- [LangChain 快速入门](../LangChain快速入门.md)
- [HelloAgents 源码](../../HelloAgents-learn_version/)
