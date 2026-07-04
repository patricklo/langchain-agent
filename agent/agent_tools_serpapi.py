from langchain_classic.memory import buffer
from langchain_classic.prompts import chat
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import chain, RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
import time
from operator import itemgetter
from typing import AsyncIterator, List
import asyncio
from langchain_community.utilities import SerpAPIWrapper


openai_api_key = "OPENAI_API_KEY"
openai_api_base = "https://apis.itedus.cn/v1/"
chat = ChatOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
    temperature=0.7,
    model="gpt-4o"
)
search = SerpAPIWrapper()
#print(search.run("刘亦菲最近一次露面？"))

from langchain_core.tools import Tool

searchTool = Tool(
    name="search",
    description="SerpAPI是一个搜索引擎结果页面API，它允许开发者和研究人员通过编程方式获取Google、Bing、Yahoo和其他搜索引擎的搜索结果。",
    func=search.run,
    )

#print(searchTool.invoke("成龙电影"))

from langchain_community.document_loaders import PyPDFLoader,TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
loader1 = TextLoader("../test_data/txt/faq-4359.txt", encoding="utf-8")
loader2 = TextLoader("../test_data/txt/faq-7923.txt", encoding="utf-8")
doc1 = loader1.load()
doc2 = loader2.load()

embeddings_path = "C:\\Users\\patrick\\Downloads\\bge-large-zh-v1.5"
embeddings = HuggingFaceEmbeddings(model_name=embeddings_path)

vectorStoreDB = FAISS.from_documents([doc1[0],doc2[0]], embedding=embeddings)

retriever = vectorStoreDB.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 1}
)

from langchain_core.tools.retriever import create_retriever_tool

retriever_tool = create_retriever_tool(retriever, "retriever", "华为商城帮助中心文档检索器，可以搜索各种华为商城相关问题的解决方案和知识")

#print(retriever_tool.invoke("众测活动"))

tools = [searchTool, retriever_tool]

#from langchain_classic import hub
from langsmith import Client
prompt = Client().pull_prompt("hwchase17/openai-functions-agent", dangerously_pull_public_prompt=True)
#print(prompt.messages)

from langchain_classic.agents import create_openai_functions_agent,AgentExecutor
agent = create_openai_functions_agent(chat, tools, prompt)
#print(agent)

agent_executor = AgentExecutor(agent=agent, tools=tools,verbose=True)
#print(agent_executor.invoke({"input":"你好！"}))
agent_executor.invoke({"input": "能给我介绍一下华为商城里的众测活动吗？"})