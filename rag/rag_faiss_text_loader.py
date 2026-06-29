from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel,RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

embeddings_path = "C:\\Users\\patrick\\Downloads\\bge-large-zh-v1.5"
embeddings = HuggingFaceEmbeddings(model_name=embeddings_path)

vectorstore = FAISS.from_texts(
    ["小明在华为工作","熊喜欢吃蜂蜜"],
    embedding=embeddings,
)

retriever = vectorstore.as_retriever()
#print(retriever.invoke("熊喜欢吃什么"))


openai_api_key = "OPENAI_API_KEY"
openai_api_base = "https://apis.itedus.cn/v1/"
chat = ChatOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
    temperature=0.7,
    model="gpt-4o"
)


template = """
只根据以下文档回答问题：
{context}

问题：{question}
"""

prompt = ChatPromptTemplate.from_template(template)

#1
# outputParser = StrOutputParser()
#
# setup_and_retrieval = RunnableParallel(
#     {
#         "context": retriever,
#         "question": RunnablePassthrough(),
#     }
# )
# chain = setup_and_retrieval | prompt | chat | outputParser

#2
# chain = (
#     {"context": retriever, "question": RunnablePassthrough()}
#     | prompt
#     | chat
#     | StrOutputParser()
# )
#print(chain.invoke("小明在哪里工作？"))

# 多额外的变量
from operator import itemgetter
template = """
只根据以下文档回答问题：
{context}

问题：{question}
回答问题请加上称呼："{name}"
"""
prompt = ChatPromptTemplate.from_template(template)

chain = (
    {"context": itemgetter("question") | retriever,
     "question": itemgetter("question"),
     "name": itemgetter("name")
     }
    | prompt
    | chat
    | StrOutputParser()
)

print(chain.invoke({"question":"小明在哪里工作？","name":"主人"}))





