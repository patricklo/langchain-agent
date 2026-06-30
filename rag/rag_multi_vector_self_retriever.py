from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAI
from langchain_community.vectorstores import Chroma

docs = [
    Document(
        page_content="一群科学家带回恐龙爆发了混乱",
        metadata={"year": 1993, "rating": 7.7, "genre": "科幻小说"},
    ),
    Document(
        page_content="故事发生在1920年北洋年间中国南方，马邦德花钱买官，购得“萨南康省”的县长一职，坐“马拉的火车”赴任途中遭马匪张麻子一行人伏击",
        metadata={"year": 2010, "director": "姜文", "rating": 8.2},
    ),
    Document(
        page_content="话说孙悟空护送唐三藏前往西天取经，半路却和牛魔王合谋要杀害唐三藏，并偷走了紫霞仙子持有的月光宝盒。观音闻讯赶到，欲除掉孙悟空以免危害苍生。唐三藏慈悲为怀，愿意一命赔一命，感化劣徒，观音遂令孙悟空五百年后投胎做人，赎其罪孽。",
        metadata={"year": 1994, "director": "刘镇伟", "rating": 8.6},
    ),
    Document(
        page_content="故事背景设定在2075年，讲述了太阳即将毁灭，毁灭之后的太阳系已经不适合人类生存，而面对绝境，人类将开启“流浪地球”计划，试图带着地球一起逃离太阳系，寻找人类新家园的故事。",
        metadata={"year": 2019, "director": "郭帆", "rating": 8.3},
    ),
    Document(
        page_content="该片讲述了耿浩和好哥们郝义一场荒诞而有趣的“寻爱之旅”。该片采用双线叙事的手法，以耿浩和康小雨婚姻破裂为叙事的起点，在郝义携耿浩前往剧组送道具途中“寻爱”的故事中，穿插着昔日康小雨孤身前往大理并与耿浩相遇的前尘往事，讲述着在现代生活中不同人群对婚姻、生活与理想的不同追求。",
        metadata={"year": 2014, "genre": "喜剧"},
    ),
]

embeddings_path = "C:\\Users\\patrick\\Downloads\\bge-large-zh-v1.5"
embeddings = HuggingFaceEmbeddings(model_name=embeddings_path)

vectorstore = Chroma.from_documents(docs, embeddings)

from langchain_classic.chains.query_constructor.base import AttributeInfo
from langchain_classic.retrievers.self_query.base import SelfQueryRetriever

metadata_field_info = [
    AttributeInfo(
        name="genre",
        description='电影的类型，["科幻小说","喜剧","剧情片","惊悚片","爱情片","动作片","动画片"]之一',
        type="string"
    ),
    AttributeInfo(
        name="year",
        description="电影上映年份",
        type="integer",
    ),
    AttributeInfo(
        name="director",
        description="电影导演的名字",
        type="string",
    ),
    AttributeInfo(
        name="rating",
        description="电影评分 1-10",
        type="float"
    )
]

document_content_description = "电影的简要概述"

openai_api_key = "OPENAI_API_KEY"
openai_api_base = "https://apis.itedus.cn/v1/"
chat = ChatOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
    temperature=0.7,
    model="gpt-4o"
)
from langchain_community.query_constructors.chroma import ChromaTranslator
retriever = SelfQueryRetriever.from_llm(
    chat,
    vectorstore,
    document_content_description,
    metadata_field_info,
structured_query_translator=ChromaTranslator(),  # 加这一行
    enable_limit=True,
    search_kwargs={"k": 2}
)

print(retriever.invoke("给我推荐一部分评分8.5分以上的电影"))