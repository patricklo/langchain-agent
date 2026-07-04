D:\Workspace\python\langchain-agent\.venv\Scripts\python.exe D:
\Workspace\python\langchain-agent\agent\agent_agent_tools_json.py
input_variables=['agent_scratchpad', 'input', 'tool_names', 'tools'] optional_variables=['chat_history']
input_types={'chat_history': list[typing.Annotated[typing.Union[
typing.Annotated[langchain_core.messages.ai.AIMessage, Tag(tag='ai')],
typing.Annotated[langchain_core.messages.human.HumanMessage, Tag(tag='human')],
typing.Annotated[langchain_core.messages.chat.ChatMessage, Tag(tag='chat')],
typing.Annotated[langchain_core.messages.system.SystemMessage, Tag(tag='system')],
typing.Annotated[langchain_core.messages.function.FunctionMessage, Tag(tag='function')],
typing.Annotated[langchain_core.messages.tool.ToolMessage, Tag(tag='tool')],
typing.Annotated[langchain_core.messages.ai.AIMessageChunk, Tag(tag='AIMessageChunk')],
typing.Annotated[langchain_core.messages.human.HumanMessageChunk, Tag(tag='HumanMessageChunk')],
typing.Annotated[langchain_core.messages.chat.ChatMessageChunk, Tag(tag='ChatMessageChunk')],
typing.Annotated[langchain_core.messages.system.SystemMessageChunk, Tag(tag='SystemMessageChunk')],
typing.Annotated[langchain_core.messages.function.FunctionMessageChunk, Tag(tag='FunctionMessageChunk')],
typing.Annotated[langchain_core.messages.tool.ToolMessageChunk, Tag(tag='ToolMessageChunk')]], FieldInfo(
annotation=NoneType, required=True, discriminator=Discriminator(discriminator=<function _get_type at
0x0000029FE0857600>, custom_error_type=None, custom_error_message=None, custom_error_context=None))]], '
agent_scratchpad': list[typing.Annotated[typing.Union[
typing.Annotated[langchain_core.messages.ai.AIMessage, Tag(tag='ai')],
typing.Annotated[langchain_core.messages.human.HumanMessage, Tag(tag='human')],
typing.Annotated[langchain_core.messages.chat.ChatMessage, Tag(tag='chat')],
typing.Annotated[langchain_core.messages.system.SystemMessage, Tag(tag='system')],
typing.Annotated[langchain_core.messages.function.FunctionMessage, Tag(tag='function')],
typing.Annotated[langchain_core.messages.tool.ToolMessage, Tag(tag='tool')],
typing.Annotated[langchain_core.messages.ai.AIMessageChunk, Tag(tag='AIMessageChunk')],
typing.Annotated[langchain_core.messages.human.HumanMessageChunk, Tag(tag='HumanMessageChunk')],
typing.Annotated[langchain_core.messages.chat.ChatMessageChunk, Tag(tag='ChatMessageChunk')],
typing.Annotated[langchain_core.messages.system.SystemMessageChunk, Tag(tag='SystemMessageChunk')],
typing.Annotated[langchain_core.messages.function.FunctionMessageChunk, Tag(tag='FunctionMessageChunk')],
typing.Annotated[langchain_core.messages.tool.ToolMessageChunk, Tag(tag='ToolMessageChunk')]], FieldInfo(
annotation=NoneType, required=True, discriminator=Discriminator(discriminator=<function _get_type at
0x0000029FE0857600>, custom_error_type=None, custom_error_message=None, custom_error_context=None))]]}
partial_variables={'chat_history': []} metadata={'lc_hub_owner': 'hwchase17', 'lc_hub_repo': 'react-chat-json', '
lc_hub_commit_hash': '9c1258e8aa8ce33bebbd62e077c143d0b06c81f3c7de732187ee61c70c1254c7'} messages=[
SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], input_types={}, partial_variables={},
template='Assistant is a large language model trained by OpenAI.\n\nAssistant is designed to be able to assist with a
wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range
of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing
it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at
hand.\n\nAssistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to
process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses
to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives,
allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.\n\nOverall,
Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on
a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a
particular topic, Assistant is here to assist.'), additional_kwargs={}), MessagesPlaceholder(
variable_name='chat_history', optional=True), HumanMessagePromptTemplate(prompt=PromptTemplate(
input_variables=['input', 'tool_names', 'tools'], input_types={}, partial_variables={},
template='TOOLS\n------\nAssistant can ask the user to use tools to look up information that may be helpful in answering
the users original question. The tools the human can use are:\n\n{tools}\n\nRESPONSE FORMAT
INSTRUCTIONS\n----------------------------\n\nWhen responding to me, please output a response in one of two formats:\n\n
**Option 1:**\nUse this if you want the human to use a tool.\nMarkdown code snippet formatted in the following schema:
\n\n
```json\n{{\n    "action": string, \\ The action to take. Must be one of {tool_names}\n    "action_input": string \\ The input to the action\n}}\n```
\n\n**Option #2:**\nUse this if you want to respond directly to the human. Markdown code snippet formatted in the
following schema:\n\n
```json\n{{\n    "action": "Final Answer",\n    "action_input": string \\ You should put what you want to return to use here\n}}\n```
\n\nUSER\'S INPUT\n--------------------\nHere is the user\'s input (remember to respond with a markdown code snippet of
a json blob with a single action, and NOTHING else):\n\n{input}'), additional_kwargs={}), MessagesPlaceholder(
variable_name='agent_scratchpad')]

Process finished with exit code 0
