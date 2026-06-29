from langchain_core.globals import set_llm_cache
from langchain_openai import ChatOpenAI
from langchain_community.cache import SQLiteCache
import time
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

openai_api_key = "OPENAI_API_KEY"
openai_api_base = "https://apis.itedus.cn/v1/"
chat = ChatOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
    temperature=0.7,
    model="gpt-4o"
)

set_llm_cache(SQLiteCache(database_path="../db/langchain.db"))

prompt = ChatPromptTemplate.from_template("请根据下面的主题写一篇小红书营销的短文：{topic}")
output_parser = StrOutputParser()

chain = prompt | chat | output_parser
# 紀錄開始時間
start_time = time.perf_counter()
chain.invoke({"topic":"旺仔小馒头"})
end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.6f} seconds")

# 紀錄開始時間
start_time = time.perf_counter()
chain.invoke({"topic":"旺仔小馒头"})
end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.6f} seconds")