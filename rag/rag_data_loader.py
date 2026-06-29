from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel,RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader

loader = TextLoader("test_data/m7.txt", encoding="utf-8")
doc = loader.load()


loader = TextLoader("test_data/m9.txt", encoding="utf-8")
doc1 = loader.load()

embeddings_path = "C:\\Users\\patrick\\Downloads\\bge-large-zh-v1.5"
embeddings = HuggingFaceEmbeddings(model_name=embeddings_path)
vectorStoreDB = FAISS.from_documents([doc[0], doc1[0]], embedding=embeddings)

print(vectorStoreDB.similarity_search("介绍一下问界M9？"))

print(vectorStoreDB.similarity_search_with_score("介绍一下问界M9？"))





