
from src.tools.tools import web_search, scrape_url
from src.pipelines.pipeline import research_pipeline
# output = web_search("latest advancements in AI technology")
# print(output)


# output = scrape_url(
#     "https://www.ibm.com/think/topics/ai-agents"
# )
# print(output)

topic = "The impact of AI on the job market in 2026"
research_pipeline(topic)