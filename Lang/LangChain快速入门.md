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
# 两段 @tool 装饰器写法的核心区别
## 一、基础版：`@tool`（无参数）
```python
@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search the customer database for records matching the query.

    Args:
        query: Search terms to look for
        limit: Maximum number of results to return
    """
    return f"Found {limit} results for '{query}'"
```
### 规则
1. **工具名称 = 函数名**：`search_database.name` → `search_database`
2. 全部配置自动推导：
   - 工具名字：直接拿函数名
   - 工具功能描述：完整读取函数的 docstring（文档注释）
   - 参数 JSON Schema：依靠函数**类型注解**自动生成
3. 适合：函数名本身表意清晰，不需要改名的场景。

## 二、自定义名称版：`@tool("web_search")`（传入字符串参数）
```python
@tool("web_search")  # 手动指定工具名称
def search(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"

print(search.name)  # 输出 web_search，不是函数名 search
```
### 规则
1. **强制覆盖工具名称**：无视函数原名`search`，工具对外名称固定为`web_search`
2. 其余逻辑不变：
   - 工具描述依然取自函数docstring
   - 参数结构依旧靠类型注解生成
3. 使用场景：
   - 函数名为了代码规范写的短名/内部命名（比如`func1`、`db_query`），但需要给大模型一个语义清晰的工具名；
   - 多个函数需要统一对外工具名、适配第三方Agent框架工具名称约定；
   - 避免函数重名冲突，对外暴露独立工具标识。

## 三、核心区别对照表
| 对比项 | `@tool` 无参写法 | `@tool("自定义名称")` 传参写法 |
|--------|------------------|-------------------------------|
| 工具Name取值 | 自动使用Python函数名 | 手动传入字符串，强制覆盖名字 |
| 函数内部命名 | 函数名=工具名，内外统一 | 代码函数名 和 Agent识别的工具名分离 |
| 工具描述 | 全部由docstring提供 | 依旧由docstring提供，不受名称修改影响 |
| 参数Schema | 由函数类型注解生成 | 完全一致，不受名称修改影响 |
| 适用场景 | 函数名语义明确，直接对外作为工具名 | 想要对外工具名和代码函数名解耦、重命名工具 |

## 四、拓展：@tool完整参数（不止改名）
`@tool`除了传字符串改名，还可以传字典自定义**名称+描述**，进一步定制：
```python
@tool({"name": "web_search", "description": "全网搜索引擎，用于联网查询实时资讯"})
def search(query: str) -> str:
    return f"Results for: {query}"
```
此时既改名字，又直接覆盖工具描述，不再依赖docstring做说明。

## 五、实战选择建议
1. 普通业务工具、函数名一看就懂 → 直接`@tool`最简写法；
2. 函数名简写、内部代号、需要给模型一个易懂的工具标识 → `@tool("xxx名称")`自定义名字；
3. 需要重度定制工具简介 → 使用字典参数一次性配置name+description。

# LangChain 预定义联网工具 Tavily 完整使用教程
## 一、Tavily 工具介绍
Tavily是LangChain官方预置的**专业AI联网搜索工具**，专门给大模型Agent做实时互联网检索，对比普通谷歌/Bing搜索优势：
1. 针对LLM做结果精简提炼，直接返回摘要文本，减少模型处理长网页压力；
2. 支持深度搜索、限定时间范围、过滤域名、图片检索；
3. 开箱即用，属于LangChain社区预定义工具，不需要自己用`@tool`手动封装搜索函数。
核心类：`TavilySearchResults`（主搜索工具）、`TavilyExtract`（网页内容精读工具）。

## 二、前置准备
### 1. 安装依赖包
```bash
pip install -U langchain-tavily langchain-openai python-dotenv
```

### 2. 获取 Tavily API Key
1. 打开官网：https://tavily.com/ 注册账号
2. 在控制台复制 `TAVILY_API_KEY`，免费额度：每月1000次搜索调用，足够学习调试。

### 3. 密钥配置（两种方式）
#### 方式1：代码内直接设置（临时测试用，不推荐上线）
```python
import os
# 配置Tavily搜索密钥
os.environ["TAVILY_API_KEY"] = "tvly-xxxx你的密钥xxxx"
# 同时配置大模型Key（OpenAI/DeepSeek等）
os.environ["OPENAI_API_KEY"] = "xxx"
```
#### 方式2：.env环境文件（规范项目写法）
新建`.env`文件写入：
```env
TAVILY_API_KEY=tvly-xxxx你的密钥xxxx
OPENAI_API_KEY=xxx
```
代码加载：
```python
from dotenv import load_dotenv
load_dotenv() # 自动读取.env变量
```

## 三、基础用法1：直接调用工具（单独搜索）
直接实例化工具执行联网搜索，不接入Agent，纯工具调用测试
```python
from langchain_tavily import TavilySearchResults

# 初始化搜索工具
tavily_tool = TavilySearchResults(
    max_results=3, # 返回搜索结果条数
    search_depth="basic", # basic基础快速搜索 / advanced深度全网检索
    include_images=False, # 是否返回图片
    time_range="week" # 限定搜索时间：day/week/month/year
)

# 执行搜索
result = tavily_tool.invoke({"query": "2026年杭州夏季高温天气情况"})
# 打印搜索结果
for item in result:
    print(f"标题：{item['title']}")
    print(f"摘要：{item['content']}")
    print(f"来源链接：{item['url']}\n")
```

## 四、基础用法2：接入Agent智能体（核心场景，模型自主决定何时联网）
把Tavily工具交给Agent，大模型判断「需要实时信息」时自动调用搜索工具，回答用户问题。
### 完整Agent可运行代码
```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearchResults
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate

# 1. 加载环境变量
load_dotenv()

# 2. 初始化大模型
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 3. 初始化Tavily搜索工具
tools = [
    TavilySearchResults(max_results=2, search_depth="basic")
]

# 4. 构造Agent提示词
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是实时资讯助手，有时效性、外部知识问题必须使用联网搜索工具，不要凭空编造内容"),
    ("user", "{input}"),
    ("agent_scratchpad", "{agent_scratchpad}")
])

# 5. 创建工具调用Agent
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True) # verbose=True打印工具调用日志

# 6. 对话测试
response = agent_executor.invoke({
    "input": "现在2026年8月，杭州最新的文旅活动有哪些？"
})
print("最终回答：", response["output"])
```
运行后控制台会打印：模型判断调用Tavily→发起联网搜索→拿到网页结果→总结回答用户。

## 五、进阶：Tavily网页精读工具（TavilyExtract）
搜索拿到链接后，用`TavilyExtract`抓取网页全文详细内容，适合深度资料整理：
```python
from langchain_tavily import TavilyExtract

extract_tool = TavilyExtract(extract_depth="basic")
# 传入网页链接，抓取正文内容
content = extract_tool.invoke({
    "urls": ["https://xxx新闻链接.com"]
})
print(content)
```

## 六、核心常用参数说明（初始化工具时配置）
| 参数 | 作用 | 可选值 |
|------|------|--------|
| `max_results` | 返回搜索结果数量 | 整数，一般2~5 |
| `search_depth` | 搜索深度 | `basic`（快、省额度）/`advanced`（深度检索，消耗更多额度） |
| `time_range` | 时效过滤 | `day`/`week`/`month`/`year` |
| `include_images` | 是否返回配图 | True/False |
| `include_domains` | 只在指定网站搜索 | `["zhihu.com","gov.cn"]` |
| `exclude_domains` | 屏蔽垃圾网站来源 | `["bilibili.com","ads.com"]` |

## 七、和自定义@tool工具对比总结
1. **Tavily预定义工具**
   - 优点：零开发、开箱即用、接口稳定、自动适配Agent工具调用格式，专门做联网搜索；
   - 适用：需要实时互联网信息、时事新闻、最新资料查询的Agent。
2. **@tool自定义函数工具**
   - 优点：完全自由定制逻辑（数据库查询、接口调用、计算函数、本地文件读取）；
   - 适用：业务内部能力（查数据库、调用内部API、本地逻辑计算）。

## 八、常见踩坑点
1. **API Key未配置报错**：必须设置`TAVILY_API_KEY`环境变量，工具不会自动读取密钥；
2. **额度耗尽**：免费版每月1000次调用，频繁调试容易用完，可在官网查看用量；
3. **模型不调用搜索工具**：System提示词明确约束「时效性问题必须联网搜索，禁止幻觉编造」，强化工具使用意愿；
4. **搜索结果太多冗余**：`max_results`控制在2~3条，避免上下文超长。
# 整体讲解：Pydantic结构化输出实体（LangChain结构化返回核心用法）
## 一、这一段代码是干嘛的？
用 **Pydantic 的 BaseModel** 定义固定JSON结构，强制大模型**不能自由乱写自然语言**，必须按照你规定的字段格式输出结构化数据（类似固定格式JSON）。
场景：联网Agent需要同时返回「回答正文+引用的网页标题+网页链接」，方便前端渲染参考文献、溯源、校验内容来源，杜绝模型乱编来源。

### 两段模型拆解
1. **Reference 子模型：单条网页引用实体**
```python
class Reference(BaseModel):
    title: str = Field(description="The title of the web page cited in the answer")
    url: str = Field(description="The url of the web page cited in the answer")
```
用来描述一条引用资料：网页标题、网页链接。

2. **AnswerInfo 顶层模型：整体返回结构**
```python
class AnswerInfo(BaseModel):
    answer: str = Field(description="The final answer for user")
    reference: list[Reference] = Field(description="The web pages cited in the answer")
```
整体结构：
- `answer`：给用户的最终文字回答
- `reference`：数组，里面是多条`Reference`引用链接（可以0条、1条、多条搜索来源）

## 二、关键字段说明
1. `BaseModel`
Pydantic核心基类，提供**数据校验、JSON序列化、自动生成JSON Schema**能力，LangChain可以读取这个Schema给模型下发格式约束。
2. `Field(description="xxx")`
给每个字段写英文说明，会被打包进格式提示词告诉大模型：这个字段该填什么内容。

## 三、模型强制输出效果（最终拿到结构化JSON）
模型不会输出一段自由文本，只会返回类似这样的结构化数据：
```json
{
  "answer": "2026年杭州暑期有多场文旅夜市活动，集中在西湖、钱江新城板块",
  "reference": [
    {
      "title": "2026杭州夏日文旅活动汇总",
      "url": "https://xxx.news1.com"
    },
    {
      "title": "杭州夜游消费季官方公告",
      "url": "https://gov.hangzhou.cn/xxx"
    }
  ]
}
```

## 四、在LangChain里怎么用（完整落地代码）
搭配`with_structured_output`绑定模型，强制模型输出我们定义的`AnswerInfo`结构：
```python
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

# 1. 定义结构化实体（截图里的代码）
class Reference(BaseModel):
    title: str = Field(description="The title of the web page cited in the answer")
    url: str = Field(description="The url of the web page cited in the answer")

class AnswerInfo(BaseModel):
    answer: str = Field(description="The final answer for user")
    reference: list[Reference] = Field(description="The web pages cited in the answer")

# 2. 初始化模型，绑定结构化输出
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
structured_llm = llm.with_structured_output(AnswerInfo)

# 3. 调用，直接拿到Pydantic对象，不用手动解析JSON
result: AnswerInfo = structured_llm.invoke("介绍2026杭州夏季文旅活动，带上来源链接")

# 直接读取字段
print("回答正文：", result.answer)
for ref in result.reference:
    print(f"来源标题：{ref.title}，链接：{ref.url}")
```

## 五、核心使用价值
1. **后端开发友好**
不用正则、字符串分割去提取模型回答里的链接，直接对象点属性取值，对接前端、数据库非常方便。
2. **约束模型行为，减少幻觉**
强制模型必须标注引用来源，回答和来源一一对应，降低模型瞎编内容、编造链接的概率。
3. **复杂业务结构化场景通用**
不止是引用来源，还可以用来做：信息抽取（姓名/电话/地址抽取）、工单分类、参数提取、表单填充、意图识别。
4. **搭配Tavily搜索工具完美适配**
之前讲的Tavily联网搜索拿到网页title+url，直接塞进`reference`数组，实现「搜索→回答→来源溯源」完整链路。

## 六、对比普通自由文本输出
- 普通输出：一段长文字，链接混杂在文本里，机器很难解析；
- 结构化Pydantic输出：强类型结构，程序可直接读取、校验、入库、展示参考文献。

## 七、拓展小知识
- 字段描述建议英文：OpenAI系列模型对英文字段描述识别更稳定，格式出错概率更低；
- 可以加字段校验：比如`url: HttpUrl`强制校验链接合法性，模型输出错误格式会直接报错重试；
- LangChain Agent也可以绑定结构化输出，让Agent最终返回固定格式结果。