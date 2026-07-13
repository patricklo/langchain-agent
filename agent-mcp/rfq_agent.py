import asyncio
import os

from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI

RFQ_TOOL_NAME = "sendNoteRFQRequest"

RFQ_SYSTEM_PROMPT = """你是 Note RFQ 助手（RFQAgent），负责帮助用户提交 Note RFQ 请求。

在调用工具 `sendNoteRFQRequest` 之前，必须确认以下三个字段齐全：
- undelryingRetutersCode：标的 Reuters 代码
- payoffCode：Payoff 代码
- currencyCode：币种代码（如 USD、CNY）

如果用户未提供完整信息，请先向用户追问缺失字段，不要猜测或编造。

调用 `sendNoteRFQRequest` 时，参数必须是一个 JSON 对象，字段名必须完全一致：
{
  "undelryingRetutersCode": "<string>",
  "payoffCode": "<string>",
  "currencyCode": "<string>"
}

收到工具响应后，用简洁的中文向用户说明提交结果。"""


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


async def build_rfq_agent():
    rfq_tools = await load_rfq_tools()
    return create_agent(
        model=_build_llm(),
        tools=rfq_tools,
        name="RFQAgent",
        system_prompt=RFQ_SYSTEM_PROMPT,
        debug=True,
    )


async def main():
    agent = await build_rfq_agent()
    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "请为标的 AAPL.O 发送 RFQ，payoff 为 DIGITAL_CALL，币种 USD"
                    ),
                }
            ]
        }
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
