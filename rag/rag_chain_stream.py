from langchain_classic.memory import buffer
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
from typing import AsyncIterator, List
import asyncio

async def async_split_into_list(
        input: AsyncIterator[str],
) -> AsyncIterator[List[str]]:
    buffer = ""
    async for chunk in input:
        buffer += chunk
        while "," in buffer:
            comma_index = buffer.find(",")
            yield [buffer[:comma_index].strip()]
            buffer = buffer[comma_index + 1:]
    yield [buffer.strip()]




async def test():
    openai_api_key = "OPENAI_API_KEY"
    openai_api_base = "https://apis.itedus.cn/v1/"
    chat = ChatOpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
        temperature=0.7,
        model="gpt-4o"
    )
    prompt = ChatPromptTemplate.from_template(
        "响应以CSV的格式返回中文列表，不要返回其他内容。请输出与{transportation}类似的交通工具"
    )

    str_chain = prompt | chat | StrOutputParser()
    list_chain = str_chain | async_split_into_list
    async for chunk in list_chain.astream({"transportation":"飞机"}):
        print(chunk, flush=True)

if __name__ == "__main__":
    asyncio.run(test())