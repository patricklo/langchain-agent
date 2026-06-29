from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel,RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader,TextLoader
from langchain_text_splitters import HTMLHeaderTextSplitter
from torch._inductor.codegen.cutlass import template

openai_api_key = "OPENAI_API_KEY"
openai_api_base = "https://apis.itedus.cn/v1/"
chat = ChatOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
    temperature=0.7,
    model="gpt-4o"
)


loader = TextLoader("test_data/html/Animation-system.html", encoding="utf-8")
doc = loader.load()

header_to_slit_on = [
    ("h1", "Header 1"),
    ("h2", "Header 2"),
    ("h3", "Header 3"),
]

html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=header_to_slit_on)
html_header_splits = html_splitter.split_text(doc[0].page_content)
#print(html_header_splits)

embeddings_path = "C:\\Users\\patrick\\Downloads\\bge-large-zh-v1.5"
embeddings = HuggingFaceEmbeddings(model_name=embeddings_path)
vectorStoreDB = FAISS.from_documents(html_header_splits, embedding=embeddings)

template = """
只根据以下文档回答问题:
{context}

问题：{question}
"""
prompt = ChatPromptTemplate.from_template(template)

retriever = vectorStoreDB.as_retriever(
    search_type="mmr",
    search_kwargs={"k":2},
)

#docs = retriever.invoke("请说说如何控制动画的播放和暂停")
#print(docs)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | chat
    | StrOutputParser()
)

print(chain.invoke("请说说如何控制动画的播放和暂停？"))