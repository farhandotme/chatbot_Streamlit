from dotenv import load_dotenv

load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("explain {topic} in simple words")

model = ChatGroq(model="llama-3.1-8b-instant")

parser = StrOutputParser()
# formatted_prompt = prompt.format_messages(topic="Machine Learning")
# response = model.invoke(formatted_prompt)

# final_output = parser.parse(response.content)
# print(response.content)

chain = prompt | model | parser

user_query = input("You: ")


response = chain.invoke({"topic": user_query})

print(response)
