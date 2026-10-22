
from langchain.agents import create_agent
from langchain_core import messages
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.tools import web_search, scrape_url 
from dotenv import load_dotenv

import os

load_dotenv()
llm = ChatOllama(
    model = "llama3.2",
    temperature = 0.3,
)
# llm  = ChatGoogleGenerativeAI(
#     model = "gemini-3.6-flash",
#     temperature = 0.3,
#     api_key = os.getenv("GEMINI_API_KEY")

# )

# 1st Agent creation 
def build_search_agent():
    return create_agent(
        model = llm,
        tools = [web_search],
        
    )


# 2nd agent
def build_scrape_agent():
    return create_agent(
        model = llm,
        tools = [scrape_url],
       
    )

#3rd Agent

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a expert research writer. Write clean, structured and insightful reports."),
    ("human", '''Write a detailed researcg report on the topic below.
Topic : {topic}

Research Gathered : 
{research}
Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)
Be detailed, factual and professional.'''),


])

writer_chain = writer_prompt | llm | StrOutputParser()



#critic chain 

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", '''
Review the research report below and evaluare it strictly.

Report: 
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
... 
'''),
])

critic_chain = critic_prompt | llm | StrOutputParser()