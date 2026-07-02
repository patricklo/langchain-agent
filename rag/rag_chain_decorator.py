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

prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         "用代数符号写出下面的方程，然后求解。 使用格式\n\n方程:...\n解决方案:...\n\n",
         ),
        ("human","{equation_statement}")
    ]
)


