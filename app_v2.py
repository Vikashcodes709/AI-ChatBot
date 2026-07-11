import streamlit as st
import google.generativeai as genai
import os
import time
from PIL import Image  
import PyPDF2
from dotenv import load_dotenv
from streamlit_mic_recorder import mic_recorder

# -----------------------------
# Load API
# -----------------------------
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Vikash AI",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------
if "chats" not in st.session_state:
    st.session_state.chats = {
        "Chat 1": []
    }

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

messages = st.session_state.chats[st.session_state.current_chat]
# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("🤖 Vikash AI")

    theme = st.toggle("🌙 Dark Mode")

    if st.button("🆕 New Chat", use_container_width=True):
        new_chat = f"Chat {len(st.session_state.chats) + 1}"
        st.session_state.chats[new_chat] = []
        st.session_state.current_chat = new_chat
        st.rerun()

    st.divider()
    st.subheader("💬 Chats")

    search = st.text_input(
    "🔍 Search Chat",
    placeholder="Search messages..."
)

    for chat in st.session_state.chats.keys():
        if st.button(chat, use_container_width=True):
            st.session_state.current_chat = chat
            st.rerun()
    st.divider()

    st.subheader("📊 Chat Stats")

user_count = sum(
    1 for msg in messages
    if msg["role"] == "user"
)

ai_count = sum(
    1 for msg in messages
    if msg["role"] == "assistant"
)

st.write(f"👤 User: {user_count}")
st.write(f"🤖 AI: {ai_count}")
st.write(f"💬 Total: {len(messages)}")

if st.button("🗑️ Delete Current Chat", use_container_width=True):

    if len(st.session_state.chats) > 1:

        del st.session_state.chats[st.session_state.current_chat]

        st.session_state.current_chat = list(st.session_state.chats.keys())[0]

    else:

        st.session_state.chats["Chat 1"] = []
        st.session_state.current_chat = "Chat 1"

    st.divider()

new_name = st.text_input(
    "✏️ Rename Current Chat",
    placeholder="Enter new chat name..."
)

if st.button("✅ Rename", use_container_width=True):

    if new_name.strip() != "":

        st.session_state.chats[new_name] = st.session_state.chats.pop(
            st.session_state.current_chat
        )

        st.session_state.current_chat = new_name

        st.rerun()

    st.divider()

    if st.button("🗑️ Clear Current Chat", use_container_width=True):
        st.session_state.chats[st.session_state.current_chat] = []
        st.rerun()

# -----------------------------
# Main Screen
# -----------------------------
if theme:
    st.markdown("""
    <style>
    .stApp{
        background-color:#121212;
        color:white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Vikash AI")
st.caption("Your Personal AI Assistant")

for message in messages:

    if search:

        if search.lower() not in message["content"].lower():
            continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your message...")

voice = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹ Stop Recording",
    just_once=True,
    use_container_width=True
)

import speech_recognition as sr
import tempfile

if voice:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(voice["bytes"])
        audio_path = f.name

    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)

    try:
        user_input = recognizer.recognize_google(audio)
        st.success(f"🎤 You said: {user_input}")
    except:
        st.error("❌ Voice could not be recognized")

if user_input:

    prompt = f"""
You are an AI assistant.

Answer the user's question only using the PDF content below.

PDF Content:
{pdf_text}

User Question:
{user_input}
"""

    with st.spinner("📄 Reading PDF..."):
        response = model.generate_content(prompt)
        st.success(response.text)

    st.stop()

uploaded_image = st.file_uploader(
    "📷 Upload an Image",
    type=["png", "jpg", "jpeg"]
)

uploaded_pdf = st.file_uploader(
    "📄 Upload PDF",
    type=["pdf"]
)

pdf_text = ""

if uploaded_pdf is not None:
    pdf_reader = PyPDF2.PdfReader(uploaded_pdf)

    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            pdf_text += text

    st.success("✅ PDF Loaded Successfully")

if uploaded_pdf:
    st.success("✅ PDF Uploaded Successfully")

pdf_text = ""

if uploaded_pdf is not None:

    pdf_reader = PyPDF2.PdfReader(uploaded_pdf)

    for page in pdf_reader.pages:
        pdf_text += page.extract_text() + "\n"

    st.success("✅ PDF Loaded Successfully")

if uploaded_image is not None:
    st.image(
        uploaded_image,
        caption="Uploaded Image",
        use_container_width=True
    )

# -----------------------------
# Send Message
# -----------------------------

if uploaded_image is not None and st.button("🔍 Analyze Image"):

    image = Image.open(uploaded_image)

    with st.spinner("🤖 Analyzing Image..."):

        try:
            response = model.generate_content([
                "Describe this image in detail.",
                image
            ])

            st.success(response.text)

        except Exception as e:
            st.error(f"Error: {e}")

if user_input:

  if uploaded_pdf is not None and pdf_text.strip():

    user_input = f"""
Use ONLY the following PDF to answer.

PDF:
{pdf_text}

Question:
{user_input}
"""

    # Save User Message
    messages.append({
        "role": "user",
        "content": user_input
    })

if (
    len(messages) == 1
    and st.session_state.current_chat.startswith("Chat")
):

    try:
        title_response = model.generate_content(
            f"Give a very short chat title (maximum 3 words) for this message:\n{user_input}"
        )

        new_title = title_response.text.strip().replace('"', "")

        st.session_state.chats[new_title] = st.session_state.chats.pop(
            st.session_state.current_chat
        )

        st.session_state.current_chat = new_title

    except:
        pass
    

    with st.chat_message("user"):
        st.markdown(user_input)

    # AI Message
    with st.chat_message("assistant"):

        placeholder = st.empty()

        with st.spinner("🤖 Vikash AI is typing..."):
            time.sleep(1)

            try:
                response = model.generate_content(user_input)
                ai_reply = response.text
            except Exception as e:
                ai_reply = f"Error: {e}"

        full_text = ""

        for word in ai_reply.split():
            full_text += word + " "
            placeholder.markdown(full_text)
            time.sleep(0.03)

    # Save AI Message
    messages.append({
        "role": "assistant",
        "content": ai_reply
    })

    st.rerun()

    # -----------------------------
# Export Chat
# -----------------------------
chat_text = ""

for msg in messages:
    role = "You" if msg["role"] == "user" else "Vikash AI"
    chat_text += f"{role}: {msg['content']}\n\n"

st.download_button(
    "📄 Export Chat (.txt)",
    data=chat_text,
    file_name=f"{st.session_state.current_chat}.txt",
    mime="text/plain",
    use_container_width=True
)

    # -----------------------------
# Footer
# -----------------------------
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.caption(f"💬 Current Chat: {st.session_state.current_chat}")

with col2:
    st.caption(f"📨 Total Messages: {len(messages)}")

st.divider()

st.caption("🚀 Vikash AI • Powered by Gemini 2.5 Flash")