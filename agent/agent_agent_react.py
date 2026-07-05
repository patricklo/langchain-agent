from langchain_classic.document_loaders import weather
from langchain_openai import ChatOpenAI, OpenAI
from langchain_classic.tools import BaseTool
import requests
from typing import Any
from langchain_classic.agents import create_react_agent,AgentExecutor
from langsmith import Client
from langchain_core.utils.function_calling import convert_to_openai_function

openai_api_key = "OPENAI_API_KEY"
openai_api_base = "https://apis.itedus.cn/v1/"
chat = ChatOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
    temperature=0,
    model="gpt-4o"
)


#这个例子有问题，后面会自己创建react prompt
prompt = Client().pull_prompt("hwchase17/react", dangerously_pull_public_prompt=True)

#print(prompt)