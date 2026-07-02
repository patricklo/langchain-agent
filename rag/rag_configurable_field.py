from langchain_classic.prompts import chat
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate,PromptTemplate
from langchain_core.runnables import chain,RunnableParallel,RunnablePassthrough,RunnableLambda
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

prompt1 = ChatPromptTemplate.from_template("给我讲一个关于 {topic} 的故事")
prompt2 = ChatPromptTemplate.from_template("{story}\n\n 对上面的这个故事进行修改，让故事变得更加口语化和幽默有趣")

@chain
def custom_chain(text):
    #chain的写法1
    prompt_val1 = prompt1.invoke({"topic": text})
    output1 = chat.invoke(prompt_val1)
    parsed_output1 = StrOutputParser().invoke(output1)

    # chain的写法2
    chain2 = prompt2 | chat | StrOutputParser()
    return chain2.invoke({"story": parsed_output1})

@chain
def custom_chain2(text):
    # chain的写法3
    chain1 = prompt1 | chat | StrOutputParser()
    parsed_output1 = chain1.invoke({"topic": text})

    chain2 = prompt2 | chat | StrOutputParser()
    return chain2.invoke({"story": parsed_output1})

@chain
def custom_chain3(text):
    # chain的写法4
    chain = prompt1 | chat | StrOutputParser() | {"story": RunnablePassthrough()} | prompt2 | chat | StrOutputParser()
    return chain.invoke({"topic": text})