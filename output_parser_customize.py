from langchain_classic.agents.structured_chat import output_parser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from typing import Iterable

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, AIMessageChunk

openai_api_key = "OPENAI_API_KEY"
openai_api_base = "https://apis.itedus.cn/v1/"
chat = ChatOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
    temperature=0.7,
    model="gpt-4o"
)

output_parser = CommaSeparatedListOutputParser()


from langchain_core.runnables import RunnableGenerator


def streaming_parse(chunks: Iterable[AIMessageChunk]) -> Iterable[str]:
    for chunk in chunks:
        yield chunk.content.swapcase()


streaming_parse = RunnableGenerator(streaming_parse)

chain = chat | streaming_parse
for chunk in chain.stream("tell me a story"):
    print(chunk, end="")