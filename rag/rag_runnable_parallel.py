from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
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

###
#不用并行步骤，总共需时：end_time - start_time
###

start_time = time.perf_counter()
outlinePromptTemplate = '''主题：{theme}
如果要根据主题写一篇文章，请列出文章的大纲。'''
outlinePrompt = ChatPromptTemplate.from_template(outlinePromptTemplate)

tipsPromptTemplate = '''主题：{theme}
如果要根据主题写一篇文章，应该需要注意哪些方面，才能把这篇文章写好。
'''
tipsPrompt = ChatPromptTemplate.from_template(tipsPromptTemplate)

query = "2024年中国经济走向与运行趋势"
strParser = StrOutputParser()
outlineChain = outlinePrompt | chat | strParser
outline = outlineChain.invoke({"theme":query})

tipsChain = tipsPrompt | chat | strParser
tips = tipsChain.invoke({"theme":query})

articlePromptTemplate = '''主题：{theme}
大纲：
{outline}

注意事项：
{tips}

请根据上面的主题、大纲和注意事项写出丰富的完整文章内容。
'''

articlePrompt = ChatPromptTemplate.from_template(articlePromptTemplate)

articleChain = articlePrompt | chat | strParser
articleChain.invoke({
    "theme":query,
    "outline":outline,
    "tips":tips
})


end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.6f} seconds")



###
#用并行步骤，总共需时：
###

start_time = time.perf_counter()

map_chain = RunnableParallel(outline=outlineChain, tips=tipsChain,theme=itemgetter("theme"))
#map_chain.invoke({"theme":query})

allChain = map_chain | articleChain | strParser
allChain.invoke({"theme":query})
#print(allChain.invoke({"theme":query}))

end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.6f} seconds")

###
#另一种并行的实现，总共需时：
###

allChain = (
    {
        "outline":outlineChain,
        "tips":tipsChain,
        "theme":itemgetter("theme")
    }
    | articlePrompt
    | chat
    | strParser
)
allChain.invoke({"theme":query})