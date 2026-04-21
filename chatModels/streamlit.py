import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq

# Page config
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 AI Chatbot - Ask me anything")
st.markdown("Ask anything. Type **exit** to stop.")

# Initialize model (same as your code)
model = ChatGroq(model="llama-3.1-8b-instant")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="You are a expert AI assistent that solves user query")
    ]
    st.session_state.chat_history = []

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    if user_input.lower() == "exit":
        st.stop()

    # Add user message (same logic)
    st.session_state.messages.append(HumanMessage(content=user_input))
    st.session_state.chat_history.append(("You", user_input))

    # Get response (same logic)
    response = model.invoke(st.session_state.messages)

    # Store response
    st.session_state.messages.append(AIMessage(content=response.content))
    st.session_state.chat_history.append(("Bot", response.content))

# Display chat
for role, msg in st.session_state.chat_history:
    if role == "You":
        with st.chat_message("user"):
            st.markdown(msg)
    else:
        with st.chat_message("assistant"):
            st.markdown(msg)
