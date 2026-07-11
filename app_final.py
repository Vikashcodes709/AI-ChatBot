import streamlit as st
import google.generativeai as genai
import os
import time
from PIL import Image
import PyPDF2
from dotenv import load_dotenv

# -----------------------------
# API SETUP
# -----------------------------
load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# -----------------------------
# PAGE
# -----------------------------
st.set_page_config(
    page_title="Vikash AI",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# SESSION
# -----------------------------
if "chats" not in st.session_state:
    st.session_state.chats = {
        "Chat 1": []
    }

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

if "theme" not in st.session_state:
    st.session_state.theme = "Light"


messages = st.session_state.chats[
    st.session_state.current_chat
]


# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:

    st.title("🤖 Vikash AI")

    theme = st.selectbox(
        "🎨 Theme",
        ["Light", "Dark"]
    )

    st.session_state.theme = theme


    if st.button(
        "🆕 New Chat",
        use_container_width=True
    ):

        new_chat = f"Chat {len(st.session_state.chats)+1}"

        st.session_state.chats[new_chat] = []

        st.session_state.current_chat = new_chat

        st.rerun()


    st.divider()

    st.subheader("💬 Chats")


    search = st.text_input(
        "🔍 Search Chat"
    )


    for chat in list(st.session_state.chats.keys()):

        if st.button(
            chat,
            use_container_width=True
        ):

            st.session_state.current_chat = chat

            st.rerun()


    st.divider()

    st.subheader("📊 Stats")


    user_msg = sum(
        1 for m in messages
        if m["role"]=="user"
    )


    ai_msg = sum(
        1 for m in messages
        if m["role"]=="assistant"
    )


    st.write(f"👤 User: {user_msg}")
    st.write(f"🤖 AI: {ai_msg}")
    st.write(f"💬 Total: {len(messages)}")
    # -----------------------------
# THEME STYLE
# -----------------------------

if st.session_state.theme == "Dark":

    st.markdown("""
    <style>
    .stApp{
        background-color:#121212;
        color:white;
    }
    </style>
    """, unsafe_allow_html=True)


# -----------------------------
# MAIN SCREEN
# -----------------------------

st.title("🤖 Vikash AI")
st.caption("Your Personal AI Assistant")


# Show Chat

for message in messages:

    if search:

        if search.lower() not in message["content"].lower():
            continue

    with st.chat_message(message["role"]):

        st.markdown(message["content"])



# -----------------------------
# FILE UPLOAD
# -----------------------------

uploaded_image = st.file_uploader(
    "📷 Upload Image",
    type=["png","jpg","jpeg"]
)


uploaded_pdf = st.file_uploader(
    "📄 Upload PDF",
    type=["pdf"]
)



# -----------------------------
# PDF READER
# -----------------------------

pdf_text = ""


if uploaded_pdf is not None:

    reader = PyPDF2.PdfReader(uploaded_pdf)

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pdf_text += text


    st.success("✅ PDF Loaded Successfully")



# -----------------------------
# IMAGE ANALYSIS
# -----------------------------

if uploaded_image is not None:

    st.image(
        uploaded_image,
        caption="Uploaded Image",
        use_container_width=True
    )


    if st.button("🔍 Analyze Image"):

        image = Image.open(uploaded_image)


        with st.spinner("🤖 Analyzing..."):

            try:

                response = model.generate_content([
                    "Describe this image in detail.",
                    image
                ])

                st.success(response.text)


            except Exception as e:

                st.error(e)



# -----------------------------
# CHAT INPUT
# -----------------------------

user_input = st.chat_input(
    "Type your message..."
)



if user_input:


    prompt = user_input


    if pdf_text.strip():

        prompt = f"""

Answer using PDF content.

PDF:
{pdf_text}


Question:
{user_input}

"""


    messages.append(
        {
            "role":"user",
            "content":user_input
        }
    )


    with st.chat_message("user"):

        st.markdown(user_input)



    with st.chat_message("assistant"):

        with st.spinner(
            "🤖 Vikash AI is typing..."
        ):

            try:

                response = model.generate_content(prompt)

                ai_reply = response.text


            except Exception as e:

                ai_reply = f"Error: {e}"


        st.markdown(ai_reply)



    messages.append(
        {
            "role":"assistant",
            "content":ai_reply
        }
    )


    st.rerun()
    # -----------------------------
# Rename Chat
# -----------------------------

st.sidebar.divider()

new_name = st.sidebar.text_input(
    "✏️ Rename Current Chat"
)

if st.sidebar.button(
    "✅ Rename",
    use_container_width=True
):

    if new_name.strip():

        st.session_state.chats[new_name] = (
            st.session_state.chats.pop(
                st.session_state.current_chat
            )
        )

        st.session_state.current_chat = new_name

        st.rerun()


# -----------------------------
# Delete Chat
# -----------------------------

if st.sidebar.button(
    "🗑️ Delete Current Chat",
    use_container_width=True
):

    if len(st.session_state.chats) > 1:

        del st.session_state.chats[
            st.session_state.current_chat
        ]

        st.session_state.current_chat = list(
            st.session_state.chats.keys()
        )[0]

    else:

        st.session_state.chats["Chat 1"] = []

        st.session_state.current_chat = "Chat 1"

    st.rerun()



# -----------------------------
# Export Chat
# -----------------------------

chat_text = ""

for msg in messages:

    role = "You" if msg["role"] == "user" else "Vikash AI"

    chat_text += (
        f"{role}: {msg['content']}\n\n"
    )


st.sidebar.download_button(
    "📄 Export Chat TXT",
    data=chat_text,
    file_name=f"{st.session_state.current_chat}.txt",
    mime="text/plain",
    use_container_width=True
)



# -----------------------------
# Footer
# -----------------------------

st.divider()

st.caption(
    "🚀 Vikash AI • Powered by Gemini 2.5 Flash"
)