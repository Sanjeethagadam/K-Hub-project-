import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
openai.api_key = os.getenv("TOGETHER_API_KEY")
openai.api_base = "https://api.together.xyz/v1"

# Model to use
MODEL = "mistralai/Mistral-7B-Instruct-v0.1"

# Streamlit config
st.set_page_config(page_title="   CHAT BOT  ")
st.title("  CHAT  BOT ")

# Clear Chat button (sidebar)
with st.sidebar:
    if st.button("🗑 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input
user_input = st.chat_input("Ask me anything...")

# Handle message
if user_input:
    st.session_state.chat_history.append(("user", user_input))

    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                *[{"role": role, "content": msg} for role, msg in st.session_state.chat_history],
            ]
        )
        bot_reply = response["choices"][0]["message"]["content"]
    except Exception as e:
        bot_reply = f"❌ Error: {str(e)}"

    st.session_state.chat_history.append(("assistant", bot_reply))

# Display chat
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)