import os
import requests
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from rich import print
from langchain.tools import tool

load_dotenv()


# weather calling api tool
@tool
def get_weather_data(city: str) -> str:
    """Get Current City Weather Data"""
    API = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}"
    response = requests.get(url)
    data = response.json()
    if data["cod"] != 200:
        return f"Could not find the {city} data..."

    desc = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    return f"Weather in {city} : {desc} and the temprature is {temp}°C"


# data = get_weather_data.invoke("bhopal")

# print(data)


# Tavily tool

tavily_client = TavilySearch(max_results=3)


@tool
def get_news(city: str) -> str:
    """Get Latest News about a city"""
    response = tavily_client.invoke(f"give the latest news of the {city}")
    results = response.get("results", [])

    if not results:
        return f"No news found for {city}"

    formatted = ""
    for i, news in enumerate(results, 1):
        formatted += f"{i}. {news.get('title', 'No Title')}\n"
        formatted += f"{news.get('content', 'No Content')}\n\n"

    return formatted


data = get_news.invoke("india")
print(data)
