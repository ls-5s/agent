# LangChain 快速入门

> 以智能天气助手为例，从零掌握 LangChain Agent 开发全流程。
>
> 标注说明：🔷 = LangChain 标准 API &nbsp;|&nbsp; 🔶 = Python 标准库 / 工程约定

---

## 1. 环境准备

### 1.1 安装依赖

```bash
pip install langchain langchain-openai python-dotenv requests
```

| 包 | 作用 | 类型 |
|---|---|---|
| `langchain` | Agent、Tool 等核心抽象 | 🔷 LangChain |
| `langchain-openai` | OpenAI 兼容接口（ChatOpenAI） | 🔷 LangChain 官方 |
| `python-dotenv` | `.env` 文件读取 | 🔶 第三方库 |
| `requests` | HTTP 请求（工具内调 API） | 🔶 第三方库 |

### 1.2 .env 环境变量 & config.py

> 🔶 这是 Python 工程惯例，不是 LangChain 语法。目的：密钥不进代码，安全管理。

```bash
# .env
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.deepseek.com/v1
MODEL_NAME=deepseek-v4-pro
```

```python
# config.py
import os                                          # 🔶 Python 标准库
from dotenv import load_dotenv                     # 🔶 第三方库 python-dotenv

load_dotenv()                                      # 🔶 读取 .env
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")     # 🔶 os.getenv 是 Python 内置
```

---

## 2. 模型对接

### 2.1 ChatOpenAI —— 🔷 LangChain 标准

```python
from langchain_openai import ChatOpenAI           # 🔷 LangChain 标准导入

llm = ChatOpenAI(                                  # 🔷 ChatOpenAI 类
    model="deepseek-v4-pro",                       # 🔷 model= 参数
    api_key="sk-xxx",                              # 🔷 api_key= 参数
    base_url="https://api.deepseek.com/v1"         # 🔷 base_url= 参数（兼容 OpenAI 格式）
)
```

> **`ChatOpenAI`** 是 LangChain 标准类，遵循 OpenAI Chat Completion API 规范。`base_url` 指向第三方兼容端点即可对接 DeepSeek、硅基流动等。

### 2.2 llm.invoke() —— 🔷 LangChain 标准调用

```python
response = llm.invoke("你好，请用一句话介绍你自己")  # 🔷 .invoke() 是 LangChain 标准方法
print(response.content)                              # 🔷 .content 返回字符串回复
```

所有 LangChain 模型都遵循统一的 `.invoke()` 接口。

---

## 3. 工具（Tool）

### 3.1 @tool 装饰器 —— 🔷 LangChain 标准

```python
from langchain.tools import tool                   # 🔷 LangChain 标准导入

@tool                                              # 🔷 @tool 装饰器：将函数注册为 LangChain 工具
def getWeather(location: str) -> str:              #    函数名 + docstring → Agent 可见的工具描述
    """查询指定城市的实时天气"""                     #    这段 docstring 决定 Agent 何时调用此工具
    ...                                            #    函数体是普通 Python，随你怎么写
```

> `@tool` 是 LangChain 唯一的工具注册语法。修饰后，函数名和 docstring 自动转为 Agent 的工具描述。

### 3.2 工具内部实现 —— 🔶 纯 Python

```python
@tool                                              # 🔷 外层：LangChain
def getWeather(location: str) -> str:
    """查询指定城市的实时天气"""
    city_coords = {"北京": (39.90, 116.41)}         # 🔶 纯 Python dict
    coords = city_coords.get(location)              # 🔶 Python 内置方法
    url = f"https://api.open-meteo.com/..."         # 🔶 拼接 URL
    resp = requests.get(url, timeout=10)            # 🔶 requests 库
    data = resp.json()                              # 🔶 JSON 解析
    return f"{location}当前温度 {data['current']['temperature_2m']}°C"  # 🔶 返回字符串
```

> `@tool` 只管"让 Agent 知道有这个工具"，工具内部做什么（调 API、查数据库、算数）完全是普通 Python，没有 LangChain 语法。

### 3.3 多工具绑定 —— 🔷 LangChain 标准

```python
tools = [getWeather, webSearch]                    # 🔷 工具列表，传给 create_agent
```

---

## 4. Agent

### 4.1 create_agent() —— 🔷 LangChain 标准

```python
from langchain.agents import create_agent          # 🔷 LangChain 标准导入

agent = create_agent(                               # 🔷 create_agent() 创建 Agent
    llm,                                            # 🔷 第一个参数：ChatModel 实例
    tools=[getWeather, webSearch]                   # 🔷 tools= 参数：工具列表
)
```

这是 LangChain 内置的 Agent 工厂函数，内部封装了 ReAct 思考-行动循环。

### 4.2 agent.invoke() —— 🔷 LangChain 标准

```python
response = agent.invoke({                           # 🔷 .invoke() 标准调用
    "messages": [                                   # 🔷 消息列表格式
        {"role": "user", "content": "杭州今天天气如何?"}
    ]
})
```

### 4.3 消息类型 —— 🔷 LangChain 标准

```python
for msg in response["messages"]:                   # 🔷 遍历消息列表
    print(f"[{msg.type}] {msg.content}")           # 🔷 .type → human/ai/tool
                                                    # 🔷 .content → 消息文本
```

| 消息类型 | 对应类 | 含义 |
|---|---|---|
| `human` | `HumanMessage` 🔷 | 用户输入 |
| `ai` | `AIMessage` 🔷 | 模型思考/回复 |
| `tool` | `ToolMessage` 🔷 | 工具执行结果 |

---

## 5. 项目结构

> 🔶 这是工程组织惯例，不是 LangChain 强制要求。你完全可以单文件写完。

```
智能天气助手/
├── .env              # 🔶 私密配置，.gitignore 排除
├── config.py         # 🔶 集中管理环境变量
├── tools.py          # 🔷 @tool 装饰器注册
├── agent.py          # 🔷 create_agent() 组装
└── main.py           # 🔷 .invoke() 调用入口
```

---

## 6. LangChain 标准 API 速查

| 语法 | 来源 |
|---|---|
| `from langchain_openai import ChatOpenAI` | 🔷 模型 |
| `ChatOpenAI(model=, api_key=, base_url=)` | 🔷 模型实例化 |
| `llm.invoke("xxx")` | 🔷 直接调用 |
| `response.content` | 🔷 获取回复 |
| `from langchain.tools import tool` | 🔷 工具导入 |
| `@tool` | 🔷 工具装饰器 |
| `from langchain.agents import create_agent` | 🔷 Agent 导入 |
| `create_agent(llm, tools=[...])` | 🔷 创建 Agent |
| `agent.invoke({"messages": [...]})` | 🔷 Agent 调用 |
| `msg.type` / `msg.content` | 🔷 消息属性 |
| `HumanMessage` / `AIMessage` / `ToolMessage` | 🔷 消息类 |

---

## 下一步

- [智能天气助手源码](./智能天气助手/) — 规范化完整项目
- [HelloAgents 源码](../HelloAgents-learn_version/) — 手写 ReAct、Plan-Solve、Reflection 底层实现
- [官方文档](https://python.langchain.com/) — LangChain 完整教程
