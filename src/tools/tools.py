
from langchain.tools import tool
import requests 
from dotenv import load_dotenv
import os
from tavily import TavilyClient 
load_dotenv()
from rich import print

import re

import trafilatura

from readability import Document

from bs4 import BeautifulSoup
from readability import Document

tavily = TavilyClient(api_key = os.getenv("TAVILY_API_KEY"))
''''''

from langchain_core.tools import tool

@tool
def web_search(query: str) -> str:
    """Search the web for recent information and return titles, URLs, and summaries."""

    response = tavily.search(query=query, max_results=5)

    # Extract the list of search-result dictionaries
    results = response["results"]

    out = []

    for r in results:
        out.append(
            f"Title: {r.get('title', 'Untitled')}\n"
            f"URL: {r.get('url', 'No URL')}\n"
            f"Snippet: {r.get('content', '')[:300]}\n"
        )

    return "\n---\n".join(out)

#     # return {
#     #     "urls" : [result.url for result in results],
#     #     "titles" : [result.title for result in results],
#     #     "content" : [result.content for result in results]
#     # }
# results = tavily.search(
#     query="latest advancements in AI technology",
#     max_results=5,
# )

# print(type(results))
# print(repr(results))


@tool 
def scrape_url(url: str) -> str:
    """
    Scrape and extract readable content from a URL.
    Uses multiple extraction strategies for reliability.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()

        html = response.text

        # Strategy 1: Trafilatura
        extracted = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=False,
        )

        if extracted and len(extracted.strip()) > 200:
            cleaned = re.sub(r"\s+", " ", extracted).strip()
            return cleaned[:5000]

        # Strategy 2: Readability
        doc = Document(html)
        clean_html = doc.summary()

        soup = BeautifulSoup(clean_html, "html.parser")

        for tag in soup([
            "script",
            "style",
            "header",
            "footer",
            "nav",
            "aside",
            "form",
        ]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        cleaned = re.sub(r"\s+", " ", text).strip()

        if len(cleaned) > 200:
            return cleaned[:5000]

        # Strategy 3: Extract text from the original HTML
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup([
            "script",
            "style",
            "header",
            "footer",
            "nav",
            "aside",
            "form",
            "noscript",
            "svg",
        ]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        cleaned = re.sub(r"\s+", " ", text).strip()

        if cleaned:
            return cleaned[:5000]

        return f"No readable content found at {url}"

    except requests.exceptions.Timeout:
        return f"Error: Request timed out while scraping {url}"

    except requests.exceptions.HTTPError as e:
        return f"Error: HTTP error while scraping {url}: {e}"

    except requests.exceptions.RequestException as e:
        return f"Error: Failed to fetch {url}: {e}"

    except Exception as e:
        return f"Error: Could not extract content from {url}: {e}"
