from langchain_classic.agents.structured_chat import output_parser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from output_parser_samples import format_instructions

openai_api_key = "OPENAI_API_KEY"
openai_api_base = "https://apis.itedus.cn/v1/"
chat = ChatOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
    temperature=0.3,
    model="gpt-4o"
)

class Book(BaseModel):
    title: str = Field(description="书的标题")
    author: str = Field(description="作者")
    description: str = Field(description="书的简介")

query = "请给我介绍学习中国历史的经典书籍"

output_parser = JsonOutputParser(
    pydantic_object=Book
)

##仅仅是因为JsonOutputParser自带的format_instructions是全英文的，中文示例，就重写成中文的format_instructions
format_instructions = """输出应格式化为符合以下JSON结构的JSON实例。。
JSON结构
```
{
'title':'书的标题',
'author':'作者',
'description':'书的简介',
}
```
"""
prompt = PromptTemplate(
    template="{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": format_instructions},
)
chain = prompt | chat | output_parser

print(chain.invoke({"query": query})) 


