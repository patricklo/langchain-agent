from langchain_classic.prompts import chat
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate,PromptTemplate
from langchain_core.runnables import RunnableParallel,RunnablePassthrough,RunnableLambda
from langchain_core.output_parsers import StrOutputParser
import time
from operator import itemgetter

openai_api_key = "OPENAI_API_KEY"
openai_api_base = "https://apis.itedus.cn/v1/"
chat = ChatOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
    temperature=0.7,
    model="gpt-4o"
)

prompt = PromptTemplate.from_template(
    """鉴于下面的用户问题，将其分类为"langchain","openAI" 或"其他"。
    不要用超过一个字来回应。
    <question>
    {question}
    </question>
    
    分类：
    """
)

chain = (
    prompt
    | chat
    | StrOutputParser()
)

#print(chain.invoke({"question":"how do I call OpenAI?"}))
langchainPrompt = PromptTemplate.from_template(
        """您是 langchain 方面的专家。 
回答问题时始终以“正如老陈告诉我的那样”开头。 
回答以下问题：

问题：{question}
回答："""
)
langchain_chain = langchainPrompt | chat

OpenAIPrompt = PromptTemplate.from_template(
        """您是 OpenAI 方面的专家。 
回答问题时始终以“正如奥特曼告诉我的那样”开头。 
回答以下问题：

问题：{question}
回答："""
)
OpenAI_chain = OpenAIPrompt | chat

generalPrompt = PromptTemplate.from_template(
        """ 回答以下问题：

问题：{question}
回答："""
)
general_chain = generalPrompt | chat


def route(info):
    if "OpenAI" in info["topic"]:
        return OpenAI_chain
    elif "LanguageChain" in info["topic"]:
        return langchain_chain
    else:
        return general_chain


full_chain = {"topic": chain, "question": lambda x: x["question"]} | RunnableLambda(route)

print(full_chain.invoke({"question": "我如何使用OpenAI的模型?"}))