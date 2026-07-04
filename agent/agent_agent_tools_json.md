D:\Workspace\python\langchain-agent\.venv\Scripts\python.exe D:
\Workspace\python\langchain-agent\agent\agent_agent_tools_json.py
first=RunnableAssign(mapper={
agent_scratchpad: RunnableLambda(lambda x: format_log_to_messages(x['intermediate_steps'],
template_tool_response=template_tool_response))
}) middle=[ChatPromptTemplate(input_variables=['agent_scratchpad', 'input'], optional_variables=['chat_history'],
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
0x00000213E8D87600>, custom_error_type=None, custom_error_message=None, custom_error_context=None))]], '
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
0x00000213E8D87600>, custom_error_type=None, custom_error_message=None, custom_error_context=None))]]},
partial_variables={'chat_history': [], 'tools': 'Weather - 查询中国城市天气。参数 city 可传中文城市名（如：广州、北京）或 6 位
adcode（如：440100）。', 'tool_names': 'Weather'}, metadata={'lc_hub_owner': 'hwchase17', 'lc_hub_repo': '
react-chat-json', 'lc_hub_commit_hash': '9c1258e8aa8ce33bebbd62e077c143d0b06c81f3c7de732187ee61c70c1254c7'}, messages=[
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
variable_name='agent_scratchpad')]), _ChatModelBinding(bound=ChatOpenAI(metadata={'lc_versions': {'langchain-core': '
1.4.8', 'langchain-openai': '1.3.3'}}, output_version=None, profile={'name': 'GPT-4o', 'release_date': '2024-05-13', '
last_updated': '2024-08-06', 'open_weights': False, 'max_input_tokens': 128000, 'max_output_tokens': 16384, '
text_inputs': True, 'image_inputs': True, 'audio_inputs': False, 'pdf_inputs': True, 'video_inputs': False, '
text_outputs': True, 'image_outputs': False, 'audio_outputs': False, 'video_outputs': False, 'reasoning_output':
False, 'tool_calling': True, 'structured_output': True, 'attachment': True, 'temperature': True, 'image_url_inputs':
True, 'pdf_tool_message': True, 'image_tool_message': True, 'tool_choice': True, 'tool_call_streaming': True}, client=<
openai.resources.chat.completions.completions.Completions object at 0x00000213A4458890>, async_client=<
openai.resources.chat.completions.completions.AsyncCompletions object at 0x00000213A4C7A330>, root_client=<openai.OpenAI
object at 0x00000213A33BCB30>, root_async_client=<openai.AsyncOpenAI object at 0x00000213A4AB7710>, model_name='gpt-4o',
temperature=0.0, model_kwargs={}, openai_api_key=SecretStr('**********'), openai_api_base='https://apis.itedus.cn/v1/',
openai_proxy=None, stream_chunk_timeout=120.0), kwargs={'stop': ['\nObservation']}, config={}, config_factories=[])]
last=JSONAgentOutputParser()

Process finished with exit code 0
