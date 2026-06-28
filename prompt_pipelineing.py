from langchain_core.prompts.prompt import PromptTemplate

full_template = """{introduction}

{example}

{start}"""

full_prompt = PromptTemplate.from_template(full_template)

introduction_template = """你正在冒充{person}。"""
introduction_prompt = PromptTemplate.from_template(introduction_template)

example_template = """
下面是一个交互示例：

Q：{example_q}
A：{example_a}"""
example_prompt = PromptTemplate.from_template(example_template)

start_template = """现在正式开始！

Q：{input}
A："""
start_prompt = PromptTemplate.from_template(start_template)

def build_pipeline_prompt(final_prompt, pipeline_prompts, variables):
    """Replaces PipelinePromptTemplate.invoke(variables)."""
    data = dict(variables)
    for name, prompt in pipeline_prompts:
        data[name] = prompt.invoke(data).to_string()
    return final_prompt.invoke(data)
# Same setup as your file...
input_prompts = [
    ("introduction", introduction_prompt),
    ("example", example_prompt),
    ("start", start_prompt),
]
# input_variables equivalent:
created = {name for name, _ in input_prompts}
all_vars = set()
for _, p in input_prompts:
    all_vars.update(p.input_variables)
print(sorted(all_vars - created))  # ['example_a', 'example_q', 'input', 'person']
# Format the full prompt:
result = build_pipeline_prompt(full_prompt, input_prompts, {
    "person": "马斯克",
    "example_q": "你最喜欢的颜色？",
    "example_a": "蓝色",
    "input": "你最喜欢的食物？",
})
print(result.to_string())