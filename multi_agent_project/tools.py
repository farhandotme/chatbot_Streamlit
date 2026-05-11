from langchain.tools import tool
from langchain_tavily import TavilySearch

from dotenv import load_dotenv
from rich import print
import requests
from bs4 import BeautifulSoup

load_dotenv()

tavily = TavilySearch(max_results=5)


@tool
def web_search(query: str) -> str:
    """Search the Web and grab he recent ,relevent and reliable information about the topic and returns Titles , URLs and content etc....."""

    result = tavily.invoke(query)

    out = []
    for r in result["results"]:
        out.append(
            f"Title : {r["title"]} \nURL : {r["url"]} \n Content : {r["content"][:300]}"
        )
    return "\n-----\n".join(out)


@tool
def scrape_url(url: str) -> str:
    """Scrape and return the clean text content from a given URL for deeper reading..."""
    try:
        response = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape url {str(e)}"
