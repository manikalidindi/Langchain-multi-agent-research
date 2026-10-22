
from src.tools.tools import web_search, scrape_url

# output = web_search("latest advancements in AI technology")
# print(output)


output = scrape_url(
    "https://www.ibm.com/think/topics/ai-agents"
)
print(output)