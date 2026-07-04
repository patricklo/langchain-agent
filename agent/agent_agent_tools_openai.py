from langchain_classic.document_loaders import weather
from langchain_openai import ChatOpenAI, OpenAI
from langchain_classic.tools import BaseTool
import requests
from typing import Any
from langchain_classic.agents import create_openai_functions_agent,AgentExecutor
from langsmith import Client
from langchain_core.utils.function_calling import convert_to_openai_function

openai_api_key = "OPENAI_API_KEY"
openai_api_base = "https://apis.itedus.cn/v1/"
chat = ChatOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
    temperature=0,
    model="gpt-4o"
)

llm = chat

class Weather(BaseTool):
    name: str = "Weather"
    description: str = (
        "查询中国城市天气。"
        "参数 city 可传中文城市名（如：广州、北京）或 6 位 adcode（如：440100）。"
    )

    def __init__(self):
        super().__init__()

    def get_weather(self, location):
        api_key = "dcc85083d8ddbf5e657a5c423f4d822b"
        #url = f"https://api.seniverse.com/v3/weather/now.json?key={api_key}&location={location}&language=zh-Hans&unit=c"
        url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={api_key}&city={location}&extensions=all"
        response = requests.get(url)
        #print(location)
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

    def _run(self, para):
        print(para)
        return self.get_weather(para)

weather_tool = Weather()
#print(weather_tool.run({"para":"110000"}))

prompt = Client().pull_prompt("hwchase17/openai-functions-agent", dangerously_pull_public_prompt=True)
tools = [weather_tool]

agent = create_openai_functions_agent(llm, tools, prompt)
print(agent)
#agent_executor = AgentExecutor(agent=agent, tools=tools,verbose=True)
#agent_executor.invoke({"input": "请查询北京110000的天气"})

# msg = llm.bind(
#     functions=[convert_to_openai_function(weather_tool)]
# ).invoke("请查询北京110000的天气")
# print(msg.additional_kwargs)  # 应有 function_call
# print(msg.content)