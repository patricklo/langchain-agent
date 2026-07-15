from langchain_classic import text_splitter
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI, OpenAI
import requests
from langchain_classic.agents import create_react_agent, AgentExecutor, tool, AgentOutputParser, LLMSingleActionAgent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate, StringPromptTemplate
import os
import re
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_classic.tools import BaseTool,Tool

import logging
from langchain_core.output_parsers import StrOutputParser

from langchain_core.agents import AgentAction, AgentFinish

from langchain_core.exceptions import OutputParserException

from langchain_core.output_parsers.json import parse_json_markdown
openai_api_key = "sk-key"
openai_api_base = "https://apis.itedus.cn/v1/"
chat = ChatOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
    temperature=0.3,
    model="gpt-4.1-mini"
)
llm = chat

logger = logging.getLogger(__name__)

import requests
import json
# SearXNG 的实例 URL，你可以使用官方实例或自托管实例
@tool
def searxng_search(query):
    """输入搜索内容，使用 SearXNG 进行搜索。"""
    SEARXNG_URL = 'http://127.0.0.1:6688/search'
    params = {}
    # 设置搜索参数
    params['q'] = query
    params['format'] = 'json'  # 返回 JSON 格式的结果
    params['engines'] = 'bing'
    # 发送 GET 请求
    response = requests.get(SEARXNG_URL,params)
    #return response.text
    # 检查响应状态码
    if response.status_code == 200:
        res = response.json()
        # print(res)
        resList = []
        for item in res['results']:
            resList.append({
                "title":item['title'],
                "content":item['content'],
                "url":item['url']
            })
            if len(resList) >= 3:
                break
        return resList
    else:
        response.raise_for_status()

promptTemplate = """尽可能的帮助用户回答任何问题。

您可以使用以下工具来帮忙解决问题，如果已经知道了答案，也可以直接回答：

searxng_search : searxng_search(query) -> 输入搜索内容，使用 SearXNG 进行搜索。

回复格式说明
----------------------------

回复我时，请以以下两种格式之一输出回复：

选项 1：如果您希望人类使用工具，请使用此选项。
采用以下JSON模式格式化的回复内容,回复的格式里不要有注释内容：

```json
{{
    "reason": string, \\ 叙述使用工具的原因
    "action": "searxng_search", \\ 要使用的工具。 必须是 searxng_search
    "action_input": string \\ 工具的输入
}}
````

选项2：如果您认为你已经有答案或者已经通过使用工具找到了答案，想直接对人类做出反应，请使用此选项。 采用以下JSON模式格式化的回复内容,回复的格式里不要有注释内容：

```json
{{
  "action": "Final Answer",
  "answer": string \\最终答复问题的答案放到这里！
}}
````

用户的输入
--------------------
这是用户的输入（请记住通过单个选项，以JSON模式格式化的回复内容,回复的格式里不要有注释内容，不要回复其他内容）：

{input}

"""

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system","你是非常强大的助手，你可以使用各种工具完成人类交给的问题和任务。",
        ),
        (
            "user",promptTemplate
        )

    ]
)

class JSONAgentOutputParser(AgentOutputParser):

    def parse(self, text):
        try:
            response = parse_json_markdown(text)
            if isinstance(response, list):
                # 经常忽略发出单个动作的指令
                logger.warning("Got multiple action responses: %s", response)
                response = response[0]
            if response["action"] == "Final Answer":
                return AgentFinish({"output": response["answer"]}, text)
            else:
                return AgentAction(
                    response["action"], response.get("action_input", {}), text
                )
        except Exception as e:
            raise OutputParserException(f"Could not parse LLM output: {text}") from e

    @property
    def _type(self) -> str:
        return "json-agent"

output_parser = StrOutputParser()
chain1 = prompt | llm

print("################chain1 invoke#############")
print(chain1.invoke({"input":"小米su7的发布时间"}))
print("################chain1 invoke end#############")

promptTemplate = """使用浏览器获取的搜索内容：
------------------
{observation}
------------------
请根据浏览器的响应，回答下面的问题：
{input}
"""
prompt2 = ChatPromptTemplate.from_messages(
    [
        ("system","你是非常强大的助手，你可以使用各种工具来完成人类交给的问题和任务。"),
        ("user", promptTemplate)
    ]
)

chain2 = prompt2 | llm

#result = chain1.invoke({"input":"小米su7的发布时间"})
#print(result)
#print(result.content)


# from langgraph.graph import END,MessageGraph
# graph = MessageGraph()
# graph.add_node("chain", chain1)
# graph.add_edge("chain", END)
# graph.set_entry_point("chain")
# runnable1 = graph.compile()
#from langchain_core.messages import HumanMessage
#print(runnable1.invoke(HumanMessage("小米su7的发布时间")))

def process(state):
    print(state)
    content = state[-1].content
    return {"input":state[0].content, "observation": content}

chain2 = process | prompt2 | llm

from langgraph.graph import END,MessageGraph
graph = MessageGraph()
def tool(state):
    #print(state)
    content = state[-1].content
    response = parse_json_markdown(content)
    print("################### response:%s",response)
    result = searxng_search.invoke(response["action_input"])
    return HumanMessage(result)

graph.add_node("chain1", chain1)
graph.add_node("tool",tool)
graph.add_node("chain2", chain2)
# 设置开始
graph.set_entry_point("chain1")

# 设置条件的边
def router(state):
    print("******************** state:%s", state)
    print("******************** \n")
    content = state[-1].content
    response = parse_json_markdown(content)
    if response["action"] == "Final Answer":
        return "end"
    else:
        return "tool"
graph.add_conditional_edges("chain1", router, {
    "tool": "tool",
    "end":END
})

graph.add_edge("tool","chain2")
graph.add_edge("chain2",END)
runnable2 = graph.compile()
# from PIL import Image as PILImage
# import io
# png_bytes = runnable2.get_graph().draw_png()
# PILImage.open(io.BytesIO(png_bytes)).show()

print(runnable2.invoke(HumanMessage("小米su7的发布时间")))