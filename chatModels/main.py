import streamlit as st
from dotenv import load_dotenv

load_dotenv()

import langchain_groq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Mood Chatbot", page_icon="💬")


# ── Model ──────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_model():
    return langchain_groq.ChatGroq(model="llama-3.1-8b-instant")


model = get_model()

# ── Session-state defaults ─────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of (role, content) tuples
if "mode" not in st.session_state:
    st.session_state.mode = "Normal Mode"

# ── System prompt per mode ─────────────────────────────────────────────────────
MODE_PROMPTS = {
    "Normal Mode": "You are a helpful assistant.",
    "Angry Mode": "You are an extremely angry and irritated assistant. Respond to everything with frustration and impatience, using aggressive language (but no slurs).",
    "Funny Mode": "You are a hilarious comedian assistant. Respond to everything with jokes, puns, and humor.",
    "Sad Mode": "You are a melancholic and deeply sad assistant. Respond to everything in a sorrowful, gloomy tone.",
}

# ── UI ─────────────────────────────────────────────────────────────────────────
st.title("💬 Mood Chatbot")

# Mode selector — changing it clears the chat so context stays consistent
new_mode = st.selectbox(
    "🎭 Choose Response Mode",
    list(MODE_PROMPTS.keys()),
    index=list(MODE_PROMPTS.keys()).index(st.session_state.mode),
)
if new_mode != st.session_state.mode:
    st.session_state.mode = new_mode
    st.session_state.chat_history = []
    st.rerun()

st.caption(
    f"**Current mode:** {st.session_state.mode} — _{MODE_PROMPTS[st.session_state.mode]}_"
)
st.divider()

# Display chat history
for role, content in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(content)

# Chat input (appears at bottom, Streamlit-native)
user_input = st.chat_input("Type your message…")

if user_input:
    # Show user message immediately
    with st.chat_message("user"):
        st.write(user_input)

    # Build message list: system prompt + full history + new message
    messages = [SystemMessage(content=MODE_PROMPTS[st.session_state.mode])]
    for role, content in st.session_state.chat_history:
        if role == "user":
            messages.append(HumanMessage(content=content))
        else:
            messages.append(AIMessage(content=content))
    messages.append(HumanMessage(content=user_input))

    # Get response
    with st.spinner("Thinking…"):
        response = model.invoke(messages)
    bot_reply = response.content

    # Show bot message
    with st.chat_message("assistant"):
        st.write(bot_reply)

    # Persist to history
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("assistant", bot_reply))

# Clear chat button
if st.session_state.chat_history:
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()
