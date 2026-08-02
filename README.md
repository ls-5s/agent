# Agent —— AI 智能体系统学习

从零到一深入理解 AI Agent，覆盖理论基础、LLM 原理、经典范式实战，以及一个完整的多智能体框架 HelloAgents 源码。

## 项目组成

```
agent/
│
├── bj/                              # 理论篇：智能体学习笔记
│   ├── 01-初识智能体.md              #   智能体定义、AIMA 五分类 vs LLM 智能体
│   ├── 02-智能体发展史.md            #   技术演进脉络
│   ├── 03-大语言模型基础.md          #   Transformer、模型调用、LLM 能力边界
│   ├── 04-智能体经典范式构建.md      #   ReAct / Plan-Solve / Reflection 手写实战
│   ├── 06-构建你的智能体框架.md      #   工程化框架设计
│   └── 07-记忆与检索.md              #   记忆系统与 RAG
│
├── HelloAgents-learn_version/       # 实战篇：多智能体框架源码
│   ├── hello_agents/
│   │   ├── agents/                  #   ReAct、Plan-Solve、Reflection 等 Agent
│   │   ├── core/                    #   LLM、消息、配置核心
│   │   ├── memory/                  #   工作/情景/语义记忆 & RAG & 向量存储
│   │   ├── tools/                   #   工具系统（搜索、计算器、终端、MCP 等）
│   │   ├── protocols/               #   MCP、A2A、ANP 协议实现
│   │   ├── rl/                      #   RL 训练（GRPO）
│   │   ├── context/                 #   上下文工程
│   │   └── evaluation/              #   BFCL、GAIA 评测基准
│   ├── examples/                    #   各章节配套示例
│   └── docs/                        #   框架 API 文档
│
└── Lang/                            # LangChain / LangGraph（待补充）
```

## 学习路线

**理论先行 → 手写范式 → 框架源码 → 进阶扩展**

1. 阅读 `bj/` 笔记，建立 Agent 知识体系
2. 按 04 章节手写 ReAct、Plan-Solve、Reflection 三大范式
3. 研读 `HelloAgents-learn_version/` 源码，理解框架设计
4. 跑通 `examples/` 示例，覆盖记忆、RAG、协议、RL

## HelloAgents 核心理念

> 除了核心 Agent 类，一切皆为 Tools。

Memory、RAG、RL、MCP 等模块统一抽象为工具，消除不必要的抽象层，回归「智能体调用工具」这一核心逻辑，真正做到快速上手与深入理解。

## 适合人群

- 想系统掌握 AI Agent 底层原理的开发者
- 准备 Agent 方向面试的求职者
- 希望从框架使用者进阶为框架开发者的工程师
