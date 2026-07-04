from langchain_openai import ChatOpenAI, OpenAI
from langchain_community.utilities import SerpAPIWrapper

openai_api_key = "OPENAI_API_KEY"
openai_api_base = "https://apis.itedus.cn/v1/"
chat = ChatOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
    temperature=0.7,
    model="gpt-4o"
)

#from langchain_classic import hub
from langsmith import Client
prompt = Client().pull_prompt("hwchase17/openai-functions-agent", dangerously_pull_public_prompt=True)
#print(prompt.messages)

from langchain_classic.agents import create_openai_functions_agent,AgentExecutor
agent = create_openai_functions_agent(chat, [], prompt)
#print(agent)

agent_executor = AgentExecutor(agent=agent, tools=[],verbose=True)

chat1_result = agent_executor.invoke({"input":"你好，我是patrick", "chat_history":[]})
from langchain_core.messages import AIMessage, HumanMessage
history = [] + [HumanMessage(content=chat1_result['input']),AIMessage(content=chat1_result['output'])]
#print(history)

# print(agent_executor.invoke({
#     "chat_history":history,
#     "input":"我的名字是什么"
# }))

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

message_history = ChatMessageHistory()
agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: message_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

agent_with_chat_history.invoke({
    "input":"你好，我是Patrick"
}, config={"configurable":{"session_id":"test_session_id"}})


print(agent_with_chat_history.invoke({
    "input":"你知道我的名字吗？"
}, config={"configurable":{"session_id":"xxxx"}})
)