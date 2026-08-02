"""
Pydantic 结构化输出实体

用 BaseModel 定义固定 JSON 结构，强制大模型按格式输出，
后端代码可以直接用对象属性取值，不用正则解析。
"""
from pydantic import BaseModel, Field


class Reference(BaseModel):
    """单条引用来源"""
    title: str = Field(description="The title of the web page cited in the answer")
    url: str = Field(description="The url of the web page cited in the answer")


class AnswerInfo(BaseModel):
    """Agent 最终回复结构"""
    answer: str = Field(description="The final answer for user")
    reference: list[Reference] = Field(description="The web pages cited in the answer")
