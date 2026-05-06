import os
import requests
from dotenv import load_dotenv

from langchain_tavily import TavilySearch
from langchain.tools import tool
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, ToolMessage

from rich import print

# Load Environment Variables
load_dotenv()


# Weather Tool
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


# Tavily News Tool
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


# AI Model
model = ChatMistralAI(model="mistral-small")


# Tools Dictionary
tools = {
    "get_weather_data": get_weather_data,
    "get_news": get_news,
}


# Bind Tools to Model
model_with_tools = model.bind_tools([get_weather_data, get_news])


# Agent Memory
messages = []


# Start Application
print("[bold green]City Intelligence System Started...[/bold green]")
print("[yellow]Type 'exit' to quit[/yellow]\n")


# Main Loop
while True:

    user_input = input("You : ")

    if user_input.lower() == "exit":
        print("\n[red]Exiting Application...[/red]")
        break

    # Add Human Message
    messages.append(HumanMessage(content=user_input))

    # Agent Loop
    while True:

        # Model Response
        result = model_with_tools.invoke(messages)

        # Save AI Message
        messages.append(result)

        # Check Tool Calls
        if hasattr(result, "tool_calls") and result.tool_calls:

            for tool_call in result.tool_calls:

                tool_name = tool_call["name"]

                print(f"\n[cyan]Tool Requested:[/cyan] {tool_name}")

                confirm = input(f"Do you want to execute '{tool_name}'? (Y/N): ")

                # Human in the loop
                if confirm.lower() in ["n", "no"]:

                    print("[red]Tool Execution Denied[/red]\n")
                    break

                try:
                    # Execute Tool
                    tool_result = tools[tool_name].invoke(tool_call["args"])

                    print("\n[green]Tool Result:[/green]")
                    print(tool_result)

                    # Add Tool Message
                    messages.append(
                        ToolMessage(content=tool_result, tool_call_id=tool_call["id"])
                    )

                except Exception as e:

                    error_message = f"Tool Execution Error: {str(e)}"

                    messages.append(
                        ToolMessage(content=error_message, tool_call_id=tool_call["id"])
                    )

            # Continue agent loop after tool execution
            continue

        else:
            # Final AI Response
            print(f"\n[bold blue]AI:[/bold blue] {result.content}\n")
            break
