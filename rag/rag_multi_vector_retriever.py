from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_core.tools import retriever
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel,RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader,TextLoader
from langchain_text_splitters import HTMLHeaderTextSplitter
from langchain_core.stores import InMemoryByteStore
from langchain_classic.retrievers.multi_vector import MultiVectorRetriever
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid


loaders = [
    TextLoader("test_data/txt/faq-4359.txt", encoding="utf-8"),
    TextLoader("test_data/txt/faq-7923.txt", encoding="utf-8"),
]

docs = []
for loader in loaders:
    docs.extend(loader.load())

embeddings_path = "C:\\Users\\patrick\\Downloads\\bge-large-zh-v1.5"
embeddings = HuggingFaceEmbeddings(model_name=embeddings_path)

# 用于索引子块的向量存储
vectorstore = Chroma(
    collection_name="full_documents",
    embedding_function=embeddings,
)
store = InMemoryByteStore()
id_key = "doc_id"
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    byte_store=store,
    id_key=id_key,
)

doc_ids =[str(uuid.uuid4()) for _ in docs]

from langchain_text_splitters import CharacterTextSplitter

child_text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=100, #100个子符分割一次
    chunk_overlap=10,
    length_function=len,
    is_separator_regex=False
)

sub_docs = []
for i, doc in enumerate(docs):
    _id = doc_ids[i]
    _sub_docs = child_text_splitter.split_documents([doc])
    for _doc in _sub_docs:
        _doc.metadata[id_key] = _id
    sub_docs.extend(_sub_docs)

retriever.vectorstore.add_documents(sub_docs)
retriever.docstore.mset(list(zip(doc_ids, docs)))

#print(retriever.vectorstore.similarity_search("众测商品多久发货呢？")[0])

openai_api_key = "OPENAI_API_KEY"
openai_api_base = "https://apis.itedus.cn/v1/"
chat = ChatOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
    temperature=0.7,
    model="gpt-4o"
)

chain = (
    {"doc": lambda x: x.page_content}
    | ChatPromptTemplate.from_template("总结下面的文档:\n\n{doc}")
    | chat
    | StrOutputParser()
)

docs = []
for loader in loaders:
    docs.extend(loader.load())

summaries = chain.batch(docs, {"max_concurrency": 5})
#print(summaries)
vectorstore = Chroma(collection_name="summaries", embedding_function=embeddings)
store = InMemoryByteStore()
id_key = "doc_id"
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    byte_store=store,
    id_key=id_key,
)
doc_ids = [str(uuid.uuid4()) for _ in docs]

summary_docs = [
    Document(page_content=s, metadata={id_key: doc_ids[i]}) for i, s in enumerate(summaries)
]
retriever.vectorstore.add_documents(summary_docs)
retriever.docstore.mset(list(zip(doc_ids, docs)))
sub_docs = retriever.vectorstore.similarity_search("众测活动是否有参与限制？")
#print(sub_docs)

sub_docs = []
for i, doc in enumerate(docs):
    _id = doc_ids[i]
    _sub_docs = child_text_splitter.split_documents([doc])
    for _doc in _sub_docs:
        _doc.metadata[id_key] = _id
    sub_docs.extend(_sub_docs)

from langchain_core.output_parsers import JsonOutputParser
###
#[ {"question":"问题1","answer":"回答1"}, {"question":"问题2","answer":"回答2"}, {"question":"问题3","answer":"回答3"} ]
#在 LangChain 里，ChatPromptTemplate.from_template() 会把 单花括号 {...} 当作模板变量。

promptStr = '''
```
{doc}
```

根据上面的文档，生成3个相关问题和回答。响应以json列表的结构返回。返回的结构参考如下
```
[
{{"question":"问题1","answer":"回答1"}},
{{"question":"问题2","answer":"回答2"}},
{{"question":"问题3","answer":"回答3"}}
]
```
'''

prompt = ChatPromptTemplate.from_template(promptStr)

chain = (
    {"doc": lambda  x : x.page_content}
    | prompt
    | chat
    | JsonOutputParser()
)

hypothetical_questions = chain.batch(sub_docs, {"max_concurrency": 5})
#print(hypothetical_questions)

documents = []
for item in hypothetical_questions:
    for obj in item:
        content = "问：{}\n答：{}".format(obj['question'],obj['answer'])
        documents.append(Document(page_content=content))

vectorstore = Chroma(collection_name="Question", embedding_function=embeddings, persist_directory="./vector_store")
store = InMemoryByteStore()
id_key = "doc_id"
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    byte_store=store,
    id_key=id_key,
)
doc_ids = [str(uuid.uuid4()) for _ in docs]
retriever.vectorstore.add_documents(documents)
print(retriever.vectorstore.similarity_search("众测商品多久发货呢？")[0])