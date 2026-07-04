D:\Workspace\python\langchain-agent\.venv\Scripts\python.exe D:
\Workspace\python\langchain-agent\agent\agent_agent_tools_xml.py
first=RunnableAssign(mapper={
agent_scratchpad: RunnableLambda(lambda x: format_xml(x['intermediate_steps']))
}) middle=[ChatPromptTemplate(input_variables=['agent_scratchpad', 'input'], input_types={},
partial_variables={'chat_history': '', 'tools': 'Weather - 查询中国城市天气。参数 city 可传中文城市名（如：广州、北京）或 6 位
adcode（如：440100）。'}, metadata={'lc_hub_owner': 'hwchase17', 'lc_hub_repo': 'xml-agent-convo', 'lc_hub_commit_hash': '
00f6b7470fa25a24eef6e4e3c1e44ba07189f3e91c4d987223ad232490673be8'}, messages=[HumanMessagePromptTemplate(
prompt=PromptTemplate(input_variables=['agent_scratchpad', 'chat_history', 'input', 'tools'], input_types={},
partial_variables={}, template="You are a helpful assistant. Help the user answer any questions.\n\nYou have access to
the following tools:\n\n{tools}\n\nIn order to use a tool, you can use <tool></tool> and <tool_input></tool_input> tags.
You will then get back a response in the form <observation></observation>\nFor example, if you have a tool called '
search' that could run a google search, in order to search for the weather in SF you would respond:\n\n<tool>
search</tool><tool_input>weather in SF</tool_input>\n<observation>64 degrees</observation>\n\nWhen you are done, respond
with a final answer between <final_answer></final_answer>. For example:\n\n<final_answer>The weather in SF is 64
degrees</final_answer>\n\nBegin!\n\nPrevious Conversation:\n{chat_history}\n\nQuestion: {input}\n{agent_scratchpad}"),
additional_kwargs={})]), _ChatModelBinding(bound=ChatOpenAI(metadata={'lc_versions': {'langchain-core': '1.4.8', '
langchain-openai': '1.3.3'}}, output_version=None, profile={'name': 'GPT-4o', 'release_date': '2024-05-13', '
last_updated': '2024-08-06', 'open_weights': False, 'max_input_tokens': 128000, 'max_output_tokens': 16384, '
text_inputs': True, 'image_inputs': True, 'audio_inputs': False, 'pdf_inputs': True, 'video_inputs': False, '
text_outputs': True, 'image_outputs': False, 'audio_outputs': False, 'video_outputs': False, 'reasoning_output':
False, 'tool_calling': True, 'structured_output': True, 'attachment': True, 'temperature': True, 'image_url_inputs':
True, 'pdf_tool_message': True, 'image_tool_message': True, 'tool_choice': True, 'tool_call_streaming': True}, client=<
openai.resources.chat.completions.completions.Completions object at 0x0000018F28648EC0>, async_client=<
openai.resources.chat.completions.completions.AsyncCompletions object at 0x0000018F28E45520>, root_client=<openai.OpenAI
object at 0x0000018F26897FE0>, root_async_client=<openai.AsyncOpenAI object at 0x0000018F286492E0>, model_name='gpt-4o',
temperature=0.0, model_kwargs={}, openai_api_key=SecretStr('**********'), openai_api_base='https://apis.itedus.cn/v1/',
openai_proxy=None, stream_chunk_timeout=120.0), kwargs={'stop': ['</tool_input>']}, config={}, config_factories=[])]
last=XMLAgentOutputParser()