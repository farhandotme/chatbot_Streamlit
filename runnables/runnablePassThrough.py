import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# --- Model ---
model = ChatGroq(model="llama-3.1-8b-instant")
outputs = StrOutputParser()

# --- Prompts ---
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

# --- Chains ---
code = code_prompt | model | outputs

explaination = RunnableParallel(
    {
        "code": RunnablePassthrough(),
        "explaination": explain_prompt | model | outputs,
    }
)

chain = code | explaination

# --- Streamlit UI ---
st.title("Code Generator + Explanation")

user_input = st.text_input("What code you want to get:")

if st.button("Generate"):
    if user_input:
        response = chain.invoke({"topic": user_input})

        st.subheader("Generated Code")
        st.code(response["code"], language="python")

        st.subheader("Explanation")
        st.write(response["explaination"])
    else:
        st.warning("Please enter a topic")
