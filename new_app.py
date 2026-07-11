import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# -----------------------------
# Load API Key
# -----------------------------
load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Vikash AI",
    page_icon="🤖",
    layout="wide",
)

# -----------------------------
# Session State
# -----------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

if "chats" not in st.session_state:
    st.session_state.chats = {
        "Chat 1": []
    }

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

messages = st.session_state.chats[
    st.session_state.current_chat
]

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.title("🤖 Vikash AI")

    theme = st.selectbox(
        "🎨 Theme",
        ["Light", "Dark"],
        index=0 if st.session_state.theme == "Light" else 1,
    )

    st.session_state.theme = theme

# -----------------------------
# Theme CSS
# -----------------------------
if st.session_state.theme == "Dark":

    st.markdown("""
    <style>
    .stApp{
        background:#121212;
        color:white;
    }
    </style>
    """, unsafe_allow_html=True)

else:

    st.markdown("""
    <style>
    .stApp{
        background:white;
        color:black;
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------
# Main Screen
# -----------------------------
# -----------------------------
# Sidebar
# -----------------------------
    st.divider()

    # New Chat
    if st.button("🆕 New Chat", use_container_width=True):
        new_chat = f"Chat {len(st.session_state.chats)+1}"
        st.session_state.chats[new_chat] = []
        st.session_state.current_chat = new_chat
        st.rerun()

    st.subheader("💬 Chats")

    # Chat List
    for chat in st.session_state.chats.keys():
        if st.button(chat, use_container_width=True):
            st.session_state.current_chat = chat
            st.rerun()

# Current Chat Messages
messages = st.session_state.chats[
    st.session_state.current_chat
]

# -----------------------------
# Theme CSS
# -----------------------------
if st.session_state.theme == "Dark":

    st.markdown("""
    <style>
    .stApp{
        background:#121212;
        color:white;
    }
    </style>
    """, unsafe_allow_html=True)

else:

    st.markdown("""
    <style>
    .stApp{
        background:white;
        color:black;
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------
# Main Screen
# -----------------------------
st.title("🤖 Vikash AI")
st.caption("Powered by Gemini 2.5 Flash")

st.subheader(f"📂 {st.session_state.current_chat}")

# Show Previous Messages
for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])