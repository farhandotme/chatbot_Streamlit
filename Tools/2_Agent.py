from langchain.tools import tool

import os
import requests

from langchain_tavily import TavilySearch

from langchain_mistralai import ChatMistralAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from dotenv import load_dotenv
from rich import print
from langchain.messages import ToolMessage
from langchain.agents.middleware import wrap_tool_call

load_dotenv()


@tool
def get_weather_data(city: str) -> str:
    """Get current weather data for a city."""

    API = os.getenv("OPENWEATHER_API_KEY")

    if not API:
        return "OpenWeather API key not found."

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API}&units=metric"
    )

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return f"Could not find weather data for {city}"

        desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]

        return (
            f"Weather in {city}:\n"
            f"- Description: {desc}\n"
            f"- Temperature: {temp}°C\n"
            f"- Feels Like: {feels_like}°C\n"
            f"- Humidity: {humidity}%"
        )

    except Exception as e:
        return f"Weather API Error: {str(e)}"


tavily_client = TavilySearch(max_results=3)


@tool
def get_news(city: str) -> str:
    """Get latest news about a city."""

    try:
        response = tavily_client.invoke(f"Give me the latest news about {city}")

        results = response.get("results", [])

        if not results:
            return f"No news found for {city}"

        formatted = ""

        for i, news in enumerate(results, 1):
            title = news.get("title", "No Title")
            content = news.get("content", "No Content")

            formatted += f"{i}. {title}\n"
            formatted += f"{content}\n\n"

        return formatted

    except Exception as e:
        return f"Tavily Error: {str(e)}"


model = ChatMistralAI(model="mistral-small")


@wrap_tool_call
def human_approval(request, handler):
    """Ask for a human approval before every tool call"""
    tool_name = request.tool_call["name"]
    confirm = input(f"Agent wants to call '{tool_name}'. Approve (Yes/No)? : ")
    if confirm.lower() != "yes":
        return ToolMessage(
            content="Tool call Denied by user...", tool_call_id=request.tool_call["id"]
        )
    return handler(request)


agent = create_agent(
    model,
    tools=[get_news, get_weather_data],
    system_prompt="You are a helpful and professional AI assistant based on city questions",
    middleware=[human_approval],
)

print("city Agent....")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
    print(result["messages"][-1].content)
