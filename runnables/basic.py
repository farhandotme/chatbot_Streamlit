from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# Prompt
prompt = ChatPromptTemplate.from_template("Explain {topic} in 1 line")

# Model
model = ChatGroq(model="llama-3.1-8b-instant")


# FIX: Extract text from AIMessage
def extract_text(ai_message):
    return ai_message.content


# Custom function
def add_exclamation(text):
    return text + "!!!"


# Runnables
extract_runnable = RunnableLambda(extract_text)
custom_runnable = RunnableLambda(add_exclamation)

# Chain
chain = prompt | model | extract_runnable | custom_runnable

# Run
result = chain.invoke({"topic": "Machine Learning"})
print(result)
