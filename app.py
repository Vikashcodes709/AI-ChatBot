import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini Model
model = genai.GenerativeModel("gemini-2.5-flash")

# Page Config
st.set_page_config(
    page_title="Vikash AI",
    page_icon="🤖",
    layout="wide"
)

# Session State

if "chats" not in st.session_state:
    st.session_state.chats = {
        "Chat 1": []
    }

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

messages = st.session_state.chats[
    st.session_state.current_chat
]

st.title("🤖 Vikash AI")
st.caption("Your Personal AI Assistant")

# Show old messages
for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
user_input = st.chat_input("Type your message...")
# Send Message
if user_input:

    # Show user message
    messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # AI Response
    with st.chat_message("assistant"):

        with st.spinner("🤖 Vikash AI is typing..."):

            try:
                response = model.generate_content(user_input)
                ai_reply = response.text
            except Exception as e:
                ai_reply = f"Error: {e}"

        st.markdown(ai_reply)

    # Save AI message
    messages.append(
        {"role": "assistant", "content": ai_reply}
    )

    st.rerun()
    # -------------------------
# Sidebar (Part 3)
# -------------------------

with st.sidebar:
    st.title("🤖 Vikash AI")

    # New Chat
    if st.button("🆕 New Chat", use_container_width=True):
      new_chat = f"Chat {len(st.session_state.chats) + 1}"
    st.session_state.chats[new_chat] = []
    st.session_state.current_chat = new_chat
    st.rerun()
    st.divider()

    st.subheader("⚙️ About")
    st.write("Model: Gemini 2.5 Flash")
    st.write("Developer: Vikash")

    # Total Messages
    st.metric(
        "Messages",
        len(messages)
    )

    st.divider()

    # Clear Chat
    if st.button("🗑️ Clear Chat", use_container_width=True):
        messages.clear() 
        st.rerun()