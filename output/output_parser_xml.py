from langchain_classic.agents.structured_chat import output_parser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import XMLOutputParser
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


actor_query = "生成汤姆·汉克斯的电影目录。"

output_parser = XMLOutputParser()
format_instructions = """响应以xml的结构返回，使用如下的xml结构
XML 文本中必须转义特殊字符：
- & 写成 &amp;
- < 写成 &lt;
- > 写成 &gt;
```
<xml>
<movie>电影1</movie>
<movie>电影2</movie>
</xml>
```
"""

prompt = PromptTemplate(
    template="""{query} \n {format_instructions}""",
    input_variables=["query"],
    partial_variables={"format_instructions": format_instructions},
)

chain = prompt | chat | output_parser

output = chain.invoke({"query": actor_query})
print(output)



