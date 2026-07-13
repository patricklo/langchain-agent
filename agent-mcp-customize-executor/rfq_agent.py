import asyncio
import json
import logging
import os

from langchain_classic.agents import AgentExecutor
from langchain_classic.agents.agent import AgentOutputParser
from langchain_classic.tools.render import render_text_description
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.output_parsers.json import parse_json_markdown
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI

RFQ_TOOL_NAME = "sendNoteRFQRequest"

TEMPLATE_TOOL_RESPONSE = """工具响应：
---------------------
{observation}

用户的输入：
---------------------
请根据工具的响应判断，是否能够回答问题：

{input}

请根据工具响应的内容，思考接下来回复。回复格式严格按照前面所说的2种JSON回复格式，选择其中1种进行回复。请记住通过单个选项，以JSON模式格式化的回复内容，不要回复其他内容。"""

PROMPT_TEMPLATE = """你是 Note RFQ 助手（RFQAgent），负责帮助用户提交 Note RFQ 请求。

您可以使用以下工具来完成任务：

{tools}

在调用工具 `sendNoteRFQRequest` 之前，必须确认以下三个字段齐全：
- undelryingRetutersCode：标的 Reuters 代码
- payoffCode：Payoff 代码
- currencyCode：币种代码（如 USD、CNY）

如果用户未提供完整信息，请直接回复追问缺失字段，不要猜测或编造。

回复格式说明
--------------------

回复我时，请以以下两种格式之一输出回复：

选项 1：如果您希望使用工具，请使用此选项。
采用以下JSON模式格式化的回复内容：

```json
{{
    "reason": string,
    "action": string,
    "action_input": string
}}
```

其中 action 必须是 {tool_names} 之一。
调用 sendNoteRFQRequest 时，action_input 必须是 JSON 字符串，字段名必须完全一致：
{{
  "undelryingRetutersCode": "<string>",
  "payoffCode": "<string>",
  "currencyCode": "<string>"
}}

选项 2：如果您认为已经有答案或者已经通过使用工具找到了答案，想直接对用户做出反应，请使用此选项。
采用以下JSON模式格式化的回复内容：

```json
{{
    "action": "Final Answer",
    "answer": string
}}
```

用户的输入
----------------------
这是用户的输入（请记住通过单个选项，以JSON模式格式化的回复内容，不要回复其他内容）：

{input}
"""

logger = logging.getLogger(__name__)


class JSONAgentOutputParser(AgentOutputParser):
    def parse(self, text):
        try:
            response = parse_json_markdown(text)
            if isinstance(response, list):
                logger.warning(response)
                response = response[0]
            if response["action"] == "Final Answer":
                return AgentFinish({"output": response["answer"]}, text)
            return AgentAction(
                response["action"],
                response.get("action_input", ""),
                text,
            )
        except Exception as e:
            raise OutputParserException(f"could not parse LLM output:{text}") from e

    @property
    def _type(self) -> str:
        return "json-agent"


def format_log_to_messages(query, intermediate_steps, template_tool_response):
    thoughts: list[BaseMessage] = []
    for action, observation in intermediate_steps:
        thoughts.append(AIMessage(content=action.log))
        thoughts.append(
            HumanMessage(
                content=template_tool_response.format(
                    input=query,
                    observation=observation,
                )
            )
        )
    return thoughts


def _build_llm() -> ChatOpenAI:
    return ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY", "OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE", "https://apis.itedus.cn/v1/"),
        temperature=0,
        model="gpt-4o",
    )


def _build_mcp_connection() -> dict:
    url = os.getenv("RFQ_MCP_URL", "http://localhost:8080/mcp")
    connection: dict = {
        "transport": "http",
        "url": url,
    }
    auth_token = os.getenv("RFQ_MCP_AUTH_TOKEN")
    if auth_token:
        connection["headers"] = {"Authorization": f"Bearer {auth_token}"}
    return connection


async def load_rfq_tools():
    client = MultiServerMCPClient({"rfq": _build_mcp_connection()})
    tools = await client.get_tools()
    rfq_tools = [tool for tool in tools if tool.name == RFQ_TOOL_NAME]
    if not rfq_tools:
        available = ", ".join(tool.name for tool in tools) or "(none)"
        raise RuntimeError(
            f"MCP tool '{RFQ_TOOL_NAME}' not found. "
            f"Check RFQ_MCP_URL and ensure the server exposes this tool. "
            f"Available tools: {available}"
        )
    return rfq_tools


def build_rfq_agent_executor(tools):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "你是非常强大的 Note RFQ 助手，你可以使用 MCP 工具来完成 RFQ 提交任务。",
            ),
            ("user", PROMPT_TEMPLATE),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    prompt = prompt.partial(
        tools=render_text_description(list(tools)),
        tool_names=", ".join(tool.name for tool in tools),
    )

    llm = _build_llm()
    agent = (
        RunnablePassthrough.assign(
            agent_scratchpad=lambda x: format_log_to_messages(
                x["input"],
                x["intermediate_steps"],
                template_tool_response=TEMPLATE_TOOL_RESPONSE,
            )
        )
        | prompt
        | llm
        | JSONAgentOutputParser()
    )
    return AgentExecutor(agent=agent, tools=tools, verbose=True)


async def main():
    tools = await load_rfq_tools()
    agent_executor = build_rfq_agent_executor(tools)
    result = agent_executor.invoke(
        {
            "input": (
                "请为标的 AAPL.O 发送 RFQ，payoff 为 DIGITAL_CALL，币种 USD"
            )
        }
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
