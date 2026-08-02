"""
项目配置模块

负责加载 .env 环境变量，统一管理所有配置项。
其他模块通过 import config 获取配置，避免硬编码。
"""
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量（API Key、接口地址等私密信息）
load_dotenv()

# 模型名称：使用 "openai:模型名" 格式强制走 OpenAI 兼容通道
# 这样 init_chat_model 自动读取 OPENAI_API_KEY 和 OPENAI_BASE_URL
MODEL_NAME = os.getenv("MODEL_NAME", "openai:deepseek-v4-pro")

# API Key：必须先在 .env 中配置 OPENAI_API_KEY
# DeepSeek 用户：在 DeepSeek 开放平台 → API Keys 获取
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# API 接口地址：DeepSeek 兼容 OpenAI 接口格式
# OpenAI 用户改为 https://api.openai.com/v1
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1")

# Tavily 搜索 API Key：在 https://tavily.com 注册免费获取
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
