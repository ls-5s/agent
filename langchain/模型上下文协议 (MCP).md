# 模型上下文协议（MCP）完整梳理重写
## 一、协议整体介绍
**模型上下文协议（Model Context Protocol，MCP）** 是一套开源标准化协议，核心作用：统一规范各类应用向大模型提供工具能力、上下文资源的交互格式。
LangChain / LangGraph 智能体可通过 `langchain-mcp-adapters` 适配器，直接调用部署在MCP服务端的全部工具函数，实现**工具与主Agent业务解耦**。

## 二、依赖安装
### 1. LangChain MCP适配器（Agent客户端侧，调用MCP工具用）
```bash
# pip安装
pip install langchain-mcp-adapters

# uv安装
uv add langchain-mcp-adapters
```
### 2. MCP服务端开发依赖（自定义工具服务）
```bash
# pip安装
pip install mcp

# uv安装
uv add mcp
```

## 三、MCP三种传输通信模式（客户端与服务端交互方式）
1. **stdio（标准输入输出）**
客户端直接拉起MCP服务作为子进程，通过控制台IO通信；适合本地轻量化工具、单机部署调试，无需端口。
2. **Streamable HTTP**
MCP以独立HTTP服务运行，支持跨机器远程调用、多客户端同时连接，适合服务化部署。
3. **SSE（Server-Sent Events）**
属于Streamable HTTP的衍生实现，针对流式实时返回场景优化，适配大模型流式输出、工具长任务推送。

## 四、LangChain客户端接入MCP工具（多服务聚合）
可以同时对接多个MCP服务（本地stdio工具+远程HTTP工具混合），统一拉取所有工具给Agent使用。
> 默认行为：无状态会话，每次调用工具新建会话，执行完成自动销毁连接。
```python
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

async def main():
    # 配置多个MCP服务：数学本地服务 + 天气远程HTTP服务
    client = MultiServerMCPClient({
        "math": {
            "transport": "stdio",
            "command": "python",
            "args": ["/path/to/math_server.py"],  # 数学MCP服务脚本绝对路径
        },
        "weather": {
            "transport": "streamable_http",
            "url": "http://localhost:8000/mcp",  # 远程天气MCP服务地址
        }
    })

    # 拉取全部MCP注册的工具
    tools = await client.get_tools()
    # 初始化大模型Agent，绑定MCP全部工具
    agent = create_agent(
        model="anthropic:claude-sonnet-4-5",
        tools=tools
    )

    # 调用数学工具问答
    math_res = await agent.ainvoke({
        "messages": [{"role": "user", "content": "(3+5)乘以12等于多少？"}]
    })
    # 调用天气工具问答
    weather_res = await agent.ainvoke({
        "messages": [{"role": "user", "content": "纽约天气如何？"}]
    })
    print(math_res, weather_res)

if __name__ == "__main__":
    asyncio.run(main())
```

## 五、自定义MCP服务端（FastMCP快速编写工具服务）
使用`FastMCP`快速将Python函数包装为标准MCP工具，支持两种运行模式。
### 示例1：数学工具服务（stdio本地进程模式 math_server.py）
```python
from mcp.server.fastmcp import FastMCP

# 初始化MCP服务，命名为Math
mcp = FastMCP("Math")

# 工具注册装饰器，函数注释自动作为工具描述给LLM识别
@mcp.tool()
def add(a: int, b: int) -> int:
    """两个数字相加"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """两个数字相乘"""
    return a * b

if __name__ == "__main__":
    # 以stdio模式启动服务
    mcp.run(transport="stdio")
```

### 示例2：天气工具服务（Streamable HTTP远程模式 weather_server.py）
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """查询指定城市天气
    :param location: 城市名称
    """
    return f"{location} 常年晴朗"

if __name__ == "__main__":
    # HTTP模式启动，可远程访问
    mcp.run(transport="streamable-http")
```

## 六、有状态MCP会话（工具需要上下文留存场景）
默认客户端是无状态短连接，若工具需要保留会话上下文（例如连续数据库查询、会话文件操作），手动创建持久化`ClientSession`。
```python
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools

async def stateful_mcp_demo():
    # 初始化MCP客户端配置
    client = MultiServerMCPClient({
        "math": {
            "transport": "stdio",
            "command": "python",
            "args": ["/path/to/math_server.py"],
        }
    })

    # 创建长生命周期会话，上下文会保留
    async with client.session("math") as session:
        tools = await load_mcp_tools(session)
        # 使用带状态的tools完成连续工具调用

if __name__ == "__main__":
    asyncio.run(stateful_mcp_demo())
```

## 七、落地总结（适配你的AI项目）
1. **架构价值**：把代码执行、文件解析、联网搜索、数据库查询拆成独立MCP服务，Agent主服务不用堆砌依赖；
2. **部署选型**：本地小工具用`stdio`，需要多服务共享工具用`streamable_http/SSE`；
3. **业务场景**：结合FastAPI + LangGraph + RAG + MCP，搭建可工具横向扩展的业务智能助手。