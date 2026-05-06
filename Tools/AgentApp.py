import os
import requests
import streamlit as st
from dotenv import load_dotenv

from langchain_tavily import TavilySearch
from langchain.tools import tool
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, ToolMessage

# =========================
# Load Environment Variables
# =========================
load_dotenv()


# =========================
# Streamlit Page Config
# =========================
st.set_page_config(page_title="City Intelligence System", page_icon="🌍", layout="wide")


# =========================
# Session State
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# =========================
# Weather Tool
# =========================
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


# =========================
# Tavily News Tool
# =========================
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


# =========================
# AI Model
# =========================
model = ChatMistralAI(model="mistral-small")


# =========================
# Tools
# =========================
tools = {
    "get_weather_data": get_weather_data,
    "get_news": get_news,
}


# =========================
# Bind Tools
# =========================
model_with_tools = model.bind_tools([get_weather_data, get_news])


# =========================
# UI
# =========================
st.title("🌍 City Intelligence System")
st.markdown("Get Weather & Latest News of Any City")


# =========================
# Display Chat History
# =========================
for role, content in st.session_state.chat_history:

    with st.chat_message(role):
        st.markdown(content)


# =========================
# Chat Input
# =========================
user_input = st.chat_input("Ask something...")


# =========================
# Main Logic
# =========================
if user_input:

    # Show User Message
    st.session_state.chat_history.append(("user", user_input))

    with st.chat_message("user"):
        st.markdown(user_input)

    # Add Human Message
    st.session_state.messages.append(HumanMessage(content=user_input))

    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        final_response = ""

        while True:

            result = model_with_tools.invoke(st.session_state.messages)

            st.session_state.messages.append(result)

            # Tool Calls
            if hasattr(result, "tool_calls") and result.tool_calls:

                for tool_call in result.tool_calls:

                    tool_name = tool_call["name"]

                    st.info(f"Calling Tool: {tool_name}")

                    try:

                        tool_result = tools[tool_name].invoke(tool_call["args"])

                        st.success(f"{tool_name} executed successfully")

                        st.code(tool_result)

                        st.session_state.messages.append(
                            ToolMessage(
                                content=tool_result, tool_call_id=tool_call["id"]
                            )
                        )

                    except Exception as e:

                        error_message = f"Tool Error: {str(e)}"

                        st.error(error_message)

                        st.session_state.messages.append(
                            ToolMessage(
                                content=error_message, tool_call_id=tool_call["id"]
                            )
                        )

                continue

            else:

                final_response = result.content

                response_placeholder.markdown(final_response)

                st.session_state.chat_history.append(("assistant", final_response))

                break
