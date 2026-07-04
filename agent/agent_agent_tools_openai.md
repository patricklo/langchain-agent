D:\Workspace\python\langchain-agent\.venv\Scripts\python.exe D:
\Workspace\python\langchain-agent\agent\agent_agent_tools_openai.py
first=RunnableAssign(mapper={
agent_scratchpad: RunnableLambda(lambda x: format_to_openai_function_messages(x['intermediate_steps']))
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
0x0000016A31067600>, custom_error_type=None, custom_error_message=None, custom_error_context=None))]], '
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
0x0000016A31067600>, custom_error_type=None, custom_error_message=None, custom_error_context=None))]]},
partial_variables={'chat_history': []}, metadata={'lc_hub_owner': 'hwchase17', 'lc_hub_repo': '
openai-functions-agent', 'lc_hub_commit_hash': 'a1655024b06afbd95d17449f21316291e0726f13dcfaf990cc0d18087ad689a5'},
messages=[SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], input_types={}, partial_variables={},
template='You are a helpful assistant'), additional_kwargs={}), MessagesPlaceholder(variable_name='chat_history',
optional=True), HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input'], input_types={},
partial_variables={}, template='{input}'), additional_kwargs={}), MessagesPlaceholder(
variable_name='agent_scratchpad')]), _ChatModelBinding(bound=ChatOpenAI(metadata={'lc_versions': {'langchain-core': '
1.4.8', 'langchain-openai': '1.3.3'}}, output_version=None, profile={'name': 'GPT-4o', 'release_date': '2024-05-13', '
last_updated': '2024-08-06', 'open_weights': False, 'max_input_tokens': 128000, 'max_output_tokens': 16384, '
text_inputs': True, 'image_inputs': True, 'audio_inputs': False, 'pdf_inputs': True, 'video_inputs': False, '
text_outputs': True, 'image_outputs': False, 'audio_outputs': False, 'video_outputs': False, 'reasoning_output':
False, 'tool_calling': True, 'structured_output': True, 'attachment': True, 'temperature': True, 'image_url_inputs':
True, 'pdf_tool_message': True, 'image_tool_message': True, 'tool_choice': True, 'tool_call_streaming': True}, client=<
openai.resources.chat.completions.completions.Completions object at 0x0000016A6C6D8A40>, async_client=<
openai.resources.chat.completions.completions.AsyncCompletions object at 0x0000016A6D008200>, root_client=<openai.OpenAI
object at 0x0000016A396A7EF0>, root_async_client=<openai.AsyncOpenAI object at 0x0000016A6C6D8AA0>, model_name='gpt-4o',
temperature=0.0, model_kwargs={}, openai_api_key=SecretStr('**********'), openai_api_base='https://apis.itedus.cn/v1/',
openai_proxy=None, stream_chunk_timeout=120.0), kwargs={'functions': [{'name': 'Weather', 'description': '查询中国城市天气。参数
city 可传中文城市名（如：广州、北京）或 6 位 adcode（如：440100）。', 'parameters': {'properties': {'para': {}}, '
required': ['para'], 'type': 'object'}}]}, config={}, config_factories=[])] last=OpenAIFunctionsAgentOutputParser()

Process finished with exit code 0
