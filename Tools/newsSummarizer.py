from dotenv import load_dotenv

load_dotenv()

from langchain_tavily import TavilySearch
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_mistralai import ChatMistralAI

tool = TavilySearch(max_results=3)

prompt = ChatPromptTemplate.from_template("""
You are a helpful AI Assistant.
Summarize the following news into clear bullet points and make a good summary that is readable by human and easy to read:

{news}
""")

model = ChatMistralAI(model="mistral-small")

chains = prompt | model | StrOutputParser()


user_input = input("Enter the News you want to search: ")

tool_calling = tool.invoke(user_input)


response = chains.invoke({"news": tool_calling})

print(response)
