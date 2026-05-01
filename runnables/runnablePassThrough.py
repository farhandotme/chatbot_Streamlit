from dotenv import load_dotenv

load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

model = ChatGroq(model="llama-3.1-8b-instant")

outputs = StrOutputParser()


code_prompt = ChatPromptTemplate.from_messages(
    [("system", "You are expert Code Generator"), ("human", "{topic}")]
)

explain_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful ai assistent that explains the code in simple terms",
        ),
        ("human", "explain the following code in simple words \n {code}"),
    ]
)

code = code_prompt | model | outputs
explaination = RunnableParallel(
    {
        "code": RunnablePassthrough(),
        "explaination": explain_prompt | model | outputs,
    }
)

chain = code | explaination

user_input = input("What code you want to get: ")
response = chain.invoke({"topic": user_input})

print(response["code"])
