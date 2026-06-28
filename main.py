# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

    prompt = ChatPromptTemplate.from_template("请根据下面的主题写一篇小红书营销的短文：{topic}")
    model = ChatOpenAI(api_key="OPENAI_API_KEY", base_url="https://apis.itedus.cn/v1/", model="gpt-4o")
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser

    print(chain.invoke({"topic":"康師傅綠茶"}))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    from huggingface_hub import snapshot_download

    snapshot_download(repo_id="BAAI/bge-large-zh-v1.5",local_dir="C:\\Users\\patrick\\Downloads\\bge-large-zh-v1.5")
    #print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
