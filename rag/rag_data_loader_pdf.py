from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel,RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from torch._inductor.codegen.cutlass import template

loader = PyPDFLoader("test_data/pdf/2312.04005.pdf")
pages = loader.load_and_split()
#print(pages)

openai_api_key = "OPENAI_API_KEY"
openai_api_base = "https://apis.itedus.cn/v1/"
chat = ChatOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
    temperature=0.7,
    model="gpt-4o"
)

docs = ""

for item in pages:
    docs += item.page_content

template = """
```
{context}
```
总结上面的论文内容
"""

prompt_template = ChatPromptTemplate.from_template(template)

#chain = prompt_template | chat | StrOutputParser()

#print(chain.invoke({"context":docs}))