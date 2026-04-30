from dotenv import load_dotenv

load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableParallel
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

shortPrompt = PromptTemplate.from_template("explain {topic} in 1-2 lines")
detailedPrompt = PromptTemplate.from_template("explain {topic} in Detailed")


model = ChatGroq(model="llama-3.1-8b-instant")

parser = StrOutputParser()

chain = RunnableParallel(
    {"short": shortPrompt | model | parser, "detailed": detailedPrompt | model | parser}
)

result = chain.invoke({"topic": "LLM"})
print()
print("Short Response : ", result["short"])
print()
print("Detailed Response : ", result["detailed"])
