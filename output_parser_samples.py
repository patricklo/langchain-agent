from langchain_classic.agents.structured_chat import output_parser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

openai_api_key = "OPENAI_API_KEY"
openai_api_base = "https://apis.itedus.cn/v1/"
chat = ChatOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
    temperature=0.7,
    model="gpt-4o"
)

output_parser = CommaSeparatedListOutputParser()

# format_instructions = output_parser.get_format_instructions()
format_instructions = "您的响应应该是csv格式的逗号分隔值的列表，例如：`内容1, 内容2, 内容3`"

prompt = PromptTemplate(
    template="{format_instructions}\n 请列出五个 {subject}",
    input_variables=["subject"],
    partial_variables={"format_instructions": format_instructions},
)

chain = prompt | chat | output_parser
#print(output_parser.get_format_instructions())

#print(chain.invoke({"subject":"冰淇淋口味"}))
#print(prompt.invoke({"subject":"冰淇淋口味"}))


#######
#from langchain_core.output_parsers.dateime import DateTimeOutputParser ##已不用
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from datetime import datetime
class TimeResponse(BaseModel):
    #Field的description会被自动翻译成给LLM的提示词
    timestamp: datetime = Field(
        description="The date and time in ISO 8601 format, strictly using '%Y-%m-%dT%H:%M:%S.%fZ'"
    )

output_parser = PydanticOutputParser(
    pydantic_object=TimeResponse,
)

template = """回答用户的问题:

{question}

{format_instructions}"""

##Option 1 start
#print(output_parser.get_format_instructions())
# prompt = PromptTemplate.from_template(
#     template,
#     partial_variables={"format_instructions": output_parser.get_format_instructions()},
# )
##Option 1 end

##Option2 start
format_instructions = """请根据用户问题推断相关日期时间，并仅返回如下 JSON（不要其他文字）：
{"timestamp": "YYYY-MM-DDTHH:MM:SS.ffffffZ"}
例如：{"timestamp": "2009-01-03T18:15:05.000000Z"}"""
prompt = PromptTemplate.from_template(
    template,
    partial_variables={"format_instructions": format_instructions},
)
##Option2 end

chain = prompt | chat | output_parser

print(chain.invoke({"question": "比特币是什么时候创立的？"}))


