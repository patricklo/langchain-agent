from langchain_openai import ChatOpenAI, OpenAI
import requests
from langchain_classic.agents import create_react_agent,AgentExecutor,tool

openai_api_key = "OPENAI_API_KEY"
openai_api_base = "https://apis.itedus.cn/v1/"
chat = ChatOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
    temperature=0,
    model="gpt-4o"
)
llm = chat

@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)


#print(get_word_length.invoke("abc"))

import requests
import json

@tool
def get_weather(location: str) -> dict:
    """Get weather for a city by adcode (e.g. '110000' for Beijing)."""
    api_key = "dcc85083d8ddbf5e657a5c423f4d822b"
    # url = f"https://api.seniverse.com/v3/weather/now.json?key={api_key}&location={location}&language=zh-Hans&unit=c"
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={api_key}&city={location}&extensions=all"
    response = requests.get(url)
    # print(location)
    print(response.json())
    if response.status_code == 200:
        data = response.json()
        weather = {
            'description': data["forecasts"][0]["casts"][0]["dayweather"],
            'temperature': data["forecasts"][0]["casts"][0]["daytemp"],
        }
        return weather
    else:
        raise Exception(f"失败接收天气信息：{response.status_code}")


#print(get_weather.invoke("110000"))

tools = [get_word_length, get_weather]

promptTemplate = """尽可能的帮助用户回答任何问题。

您可以使用以下工具来帮忙解决问题，如果已经知道了答案，也可以直接回答：

{tools}

回复格式说明
--------------------

回复我时，请以以下两种格式之一输出回复：

选项 1：如果您希望人类使用工具，请使用此选项。
采用以下JSON模式格式化的回复内容：

```json
{{
    "reason": string, \\ 叙述使用工具的原因
    "action: string, \\要使用的工具，必须是{tool_names}之一
    “action_input": string \\工具的输入
}}
```

选项 2：如果您认为你已经有答案或者已经通过使用工具找到了答案，想直接对人类做出反应，请使用此选项。采用以下JSON模式格式化的回复内容：

```json
{{
    "action": "Final Answer",
    "answer": string \\最终答复问题的答案放在这里！
}}
```

用户的输入
----------------------
这是用户的输入（请记住通过单个选项，以JSON模式格式化的回复内容，不要回复其他内容）：

{input}

"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是非常强大的助手，你可以使用各种工具来完成人类交给的问题和任务。"
        ),
        ("user", promptTemplate),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

from langchain_classic.tools.render import render_text_description

#设置工具以及工具名称
prompt = prompt.partial(
    tools = render_text_description(list(tools)),
    tool_names = ", ".join([t.name for t in tools]),
)


from langchain_classic.agents.json_chat.prompt import TEMPLATE_TOOL_RESPONSE
print(TEMPLATE_TOOL_RESPONSE)

#不使用英文版的TEMPLATE_TOOL_RESPONSE，转成中文版
TEMPLATE_TOOL_RESPONSE = """工具响应：
---------------------
{observation}

用户的输入：
---------------------
请根据工具的响应判断，是否能够回答问题：

{input}

请根据工具响应的内容，思考接下来回复。回复格式严格按照前面所说的2种JSON回复格式，选择其中1种进行回复。请记住通过单个选项，以JSON模式格式化的回复内容，不要回复其他内容。"""
import logging
logger = logging.getLogger(__name__)
from langchain_core.messages import AIMessage,BaseMessage, HumanMessage
def format_log_to_messages(
        query,
        intermediate_steps,
        template_tool_response,
):
    """Construct the scratchpad that lets the agent continue its thought process."""
    thoughts: list[BaseMessage] = []
    for action,observation in intermediate_steps:
        thoughts.append(AIMessage(content=action.log))
        human_message = HumanMessage(content=template_tool_response.format(input=query, observation=observation))
        thoughts.append(human_message)
    return thoughts

from langchain_classic.agents.agent import AgentOutputParser
from langchain_core.output_parsers.json import parse_json_markdown
from langchain_core.exceptions import OutputParserException
from langchain_core.agents import AgentAction,AgentFinish
class JSONAgentOutputParser(AgentOutputParser):
    """Parsers tool invocations and final answers in JSON format.

    Expects output to be in one of two formats:

    If the output signals that an action should be taken,
    should be in the below format, This will result in an AgentAction being returned.

    ```
    {
        "action": "search",
        "action_input": "2+2",
    }
    ```

    If the output signals that a final answer should be given,
    should be in the below format. This will resutl in an AgentFinish being returned.

    ```
    {
        "action": "Final Answer",
        "answer": "4"
    }
    ```
    """
    def parse(self, text):
        try:
            reponse = parse_json_markdown(text)
            if isinstance(reponse, list):
                #gpt turbo frequently ignores the directive amd emit a single action
                logger.warning(reponse)
                reponse = reponse[0]
            if reponse["action"] == "Final Answer":
                return AgentFinish({"output": reponse["answer"]}, text)
            else:
                return AgentAction(reponse["action"], reponse.get("action_input", ""), text)
        except Exception as e:
            raise OutputParserException(f"could not parse LLM output:{text}") from e

    @property
    def _type(self) -> str:
        return "json-agent"

from langchain_core.runnables import Runnable, RunnablePassthrough

agent = (
    RunnablePassthrough.assign(
        agent_scratchpad = lambda x: format_log_to_messages(
            x["input"],
            x["intermediate_steps"],
            template_tool_response=TEMPLATE_TOOL_RESPONSE,
            )
        )
        | prompt
        | llm
        | JSONAgentOutputParser()
)

from langchain_classic.agents import AgentExecutor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke({"input":"北京110000的天气如何？"})