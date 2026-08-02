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
# init_chat_model 知识点总结
## 一、核心定位
LangChain 官方**大模型统一初始化工厂函数**，用来抹平各家大模型SDK的初始化差异，实现「一行模型名称切换模型」，替代各个厂商独立的模型类（ChatOpenAI、ChatZhipuAI、ChatDeepSeek等）手动实例化。

## 二、核心能力
1. **厂商自动识别**
依靠模型名称前缀自动匹配对应模型服务商：
`gpt-*`→OpenAI、`deepseek-*`→深度求索、`glm-*`→智谱AI、`qwen-*`→通义千问等。
2. **配置自动加载**
默认自动读取系统环境变量（如`OPENAI_API_KEY`、`OPENAI_BASE_URL`），不用硬编码密钥、接口地址。
3. **兼容自定义参数**
既可以极简调用只传模型名，也可以传入`api_key/base_url/temperature/max_tokens`等精细化参数自定义模型行为。
4. **输出标准统一实例**
返回统一的BaseChatModel对象，可无缝接入Agent、Chain、Prompt、RAG等全部LangChain组件。

## 三、两种使用写法
### 极简模式（推荐快速开发）
```python
from langchain.chat_models import init_chat_model
llm = init_chat_model(model="deepseek-chat")
```
### 自定义配置模式
```python
llm = init_chat_model(
    model="gpt-4o",
    api_key="sk-xxx",
    base_url="代理地址",
    temperature=0
)
```

## 四、对比原生模型类（ChatOpenAI）优缺点
### 优点
1. 低耦合：切换模型仅修改模型名字符串，无需修改导入与实例代码；
2. 代码简洁：省去大量重复配置代码；
3. 多模型实验友好，批量测试不同模型效果成本极低。

### 缺点
1. 底层定制能力弱于原生类，特殊模型独有参数配置不方便；
2. 模型命名需要遵循框架识别规则，小众自定义部署模型适配较差。

## 五、适用场景
✅ 适合：项目原型开发、多模型横向对比、通用Agent业务、快速调试
❌ 适合：私有化部署模型深度定制、大模型专属高级参数调优场景（使用原生模型类）

## 六、配套Agent使用
直接将初始化后的llm传入agent创建函数，完全兼容：
```python
agent = create_agent(llm, tools=[天气工具])
```

## 💡解答
### 一、核心概念
1. **invoke（阻塞调用）**
执行时会阻塞程序，必须等待大模型把**完整内容全部生成完毕**，才一次性把整条结果返回。
用户要等很久才能看到整段回答，看不到中间打字过程。

2. **stream（流式调用）**
模型生成一个字（Token）就立刻返回一个字，结果分段实时推送，能实现网页里“打字机”逐字输出的效果。

---

### 二、关键区别对比
| 方式 | 执行特点 | 返回形式 | 用户体验 | 适用场景 |
|------|----------|----------|----------|----------|
| invoke | 阻塞等待，一次性拿到全部内容 | 完整的消息对象 | 长时间空白，最后一次性出答案 | 后台计算、批量任务、简短问答、调试代码 |
| stream | 分段实时输出，边生成边推送 | 迭代器，逐个片段返回 | 逐字弹出，和ChatGPT界面一致 | 前端对话页面、长文本写作、人机实时交互 |

---

### 三、代码示例（LangChain）
1. invoke写法
```python
# 等待全部生成完再一次性返回
result = model.invoke("讲一个小故事")
print(result.content)
```

2. stream写法
```python
# 循环遍历每一段实时输出
for chunk in model.stream("讲一个小故事"):
    print(chunk.content, end="")
```

---

### 四、补充知识点
- 内存优化：`stream`不用把整篇文本存到内存里，生成一段释放一段，长文本生成时内存占用更低。
- 异步版本：还有`ainvoke`（异步阻塞）、`astream`（异步流式），用来做Web高并发接口。
- 全链路流式：如果是Chain，必须整条链路所有组件都支持流式，否则依然会变成阻塞等待。

---

### 一句话记忆
invoke = 等全文写完再一起发；
stream = 写一个字就发一个字，实时打字。

要不要我把`invoke/stream/ainvoke/astream`这4种调用整理成一张速查表？

# LangChain 消息类型（BaseMessage体系）知识点总结
## 一、顶层父类：BaseMessage
1. **定位**：所有对话消息的顶层抽象基类，是Agent、对话上下文最基础的存储单元，统一封装角色、内容、附加元数据、工具调用信息。
2. **使用原则**：业务代码**不会直接实例化BaseMessage**，直接使用它的四大子类。

## 二、四大核心子类（按对话流转顺序）
### 1. SystemMessage
- 角色role：`system`
- 作用：给大模型设定固定人设、规则、背景、约束（系统提示词），对话全程生效。
- 示例：`你是专业天气预报助手，回答简洁直白`

### 2. HumanMessage
- 角色role：`user`
- 作用：承载用户提问、用户输入内容。
- 示例：`杭州今天多少度？`

### 3. AIMessage
- 角色role：`assistant`
- 作用：大模型返回的回复，承载两类核心数据
  1. 普通文本回答内容
  2. 工具调用结构体（模型决定要调用工具时，会把工具名称、入参放在这个消息里）
- 场景：模型直接回答话术 / 模型下发工具调用指令

### 4. ToolMessage
- 角色role：`tool`
- 作用：工具执行后的返回结果，把工具结果回传给大模型，完成ReAct循环闭环。
- 场景：调用天气接口拿到温度后，用ToolMessage把气温数据塞回对话上下文。

## 三、完整对话流转案例（ReAct工具调用闭环）
1. `SystemMessage`：设定Agent规则
2. `HumanMessage`：用户提问
3. `AIMessage`：模型判断需要调用工具，输出工具调用指令
4. `ToolMessage`：工具执行结果回填上下文
5. `AIMessage`：模型结合工具结果，输出最终回答

## 四、代码使用示例
```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage

# 组装对话上下文
messages = [
    SystemMessage(content="你是天气助手"),
    HumanMessage(content="查询杭州天气"),
    # 模型输出工具调用
    AIMessage(content="", tool_calls=[{"name":"get_weather", "args":{"city":"杭州"}}]),
    # 工具返回结果
    ToolMessage(content="杭州气温32℃，晴", tool_call_id="xxx"),
]
```

## 五、核心价值
1. **上下文标准化**：统一格式对接所有大模型，不用手动拼接`role/content`JSON结构；
2. **记忆组件兼容**：Memory记忆模块直接识别这四类消息，自动存储、截断对话历史；
3. **Agent工具调用原生适配**：AIMessage承载工具调用、ToolMessage承载工具结果，是LangChain工具Agent的底层数据基础；
4. **LangGraph状态流转友好**：对话历史直接以`List[BaseMessage]`存入全局State，实现多轮对话状态持久化。

## 六、补充拓展
还有少量特殊消息子类：
- `FunctionMessage`：旧版本函数调用遗留消息（已被ToolMessage淘汰）
- `ChatMessage`：自定义任意role角色，用于多角色模拟等特殊场景。