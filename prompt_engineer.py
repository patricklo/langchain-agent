# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from langchain_core.prompts import FewShotPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings

from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_community.vectorstores import Chroma

def print_hi(name):
    examples = [
        {
            "question": "乾隆和曹操谁活得更久?",
            "answer": """
    这里是否需要跟进问题：是的。
    追问：乾隆去世时几岁？
    中间答案：乾隆去世时87岁。
    追问：曹操去世时几岁？
    中间答案：曹操去世时66岁。
    所以最终答案是：乾隆
    """,
        },
        {
            "question": "小米手机的创始人什么时候出生?",
            "answer": """
    这里是否需要跟进问题：是的。
    追问：小米手机的创始人是谁？
    中间答案：小米手机 由 雷军 创立。
    跟进：雷军什么时候出生？
    中间答案：雷军出生于 1969 年 12 月 16 日。
    所以最终的答案是：1969 年 12 月 16 日
    """,
        },
        {
            "question": "乔治·华盛顿的外祖父是谁？",
            "answer": """
    这里是否需要跟进问题：是的。
    追问：乔治·华盛顿的母亲是谁？
    中间答案：乔治·华盛顿的母亲是玛丽·鲍尔·华盛顿。
    追问：玛丽·鲍尔·华盛顿的父亲是谁？
    中间答案：玛丽·鲍尔·华盛顿的父亲是约瑟夫·鲍尔。
    所以最终答案是：约瑟夫·鲍尔
    """,
        },
        {
            "question": "《大白鲨》和《皇家赌场》的导演是同一个国家的吗？",
            "answer": """
    这里是否需要跟进问题：是的。
    追问：《大白鲨》的导演是谁？
    中间答案：《大白鲨》的导演是史蒂文·斯皮尔伯格。
    追问：史蒂文·斯皮尔伯格来自哪里？
    中间答案：美国。
    追问：皇家赌场的导演是谁？
    中间答案：《皇家赌场》的导演是马丁·坎贝尔。
    跟进：马丁·坎贝尔来自哪里？
    中间答案：新西兰。
    所以最终的答案是：不会
    """,
        },
    ]
    example_prompt = PromptTemplate(
        input_variables=["question", "answer"],
        template="Question: {question}\n{answer}",
    )

    #print(example_prompt.format(**examples[0]))
    prompt = FewShotPromptTemplate(
        examples = examples,
        example_prompt= example_prompt,
        suffix="Question:{input}",
        input_variables=["input"],
    )
    #print(prompt.format(input="李白和白居易谁活得的更久？"))
    openai_api_key ="OPENAI_API_KEY"
    openai_api_base = "https://apis.itedus.cn/v1/"
    chat = ChatOpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
        temperature=0.7, model="gpt-4o"
    )
    output_parser = StrOutputParser()
    #chain = prompt | chat | output_parser
    #chain.invoke({"input":"李白和白居易谁活得的更久？"})

    embeddings_path = "C:\\Users\\patrick\\Downloads\\bge-large-zh-v1.5"
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_path)
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        embeddings,
        Chroma,
        k=1
    )

    #question = "李白和白居易谁活得的更久？"
    #select_examples = example_selector.select_examples({"question":question})
    #print(select_examples)

    prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix="根据案例的方式回答问题。\n",
        suffix="Question:{input}",
        input_variables=["input"],
    )

    chain = prompt | chat | output_parser
    print(chain.invoke({"input":"李白和白居易谁活得的更久？"}))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
