import streamlit as st
import json
import os
from groq import Groq

# ----------------------------
# CONFIG
# ----------------------------
st.set_page_config(page_title="AI Memory Chatbot", page_icon="🤖")

st.title("🤖 AI Memory Chatbot")
st.write("Chat with AI that remembers!")

# ----------------------------
# GROQ API SETUP
# ----------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ----------------------------
# MEMORY FILE
# ----------------------------
MEMORY_FILE = "chat_history.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f)

if "messages" not in st.session_state:
    st.session_state.messages = load_memory()

# ----------------------------
# CLEAR CHAT BUTTON
# ----------------------------
if st.button("🧹 Clear Chat"):
    st.session_state.messages = []
    save_memory([])
    st.rerun()

# ----------------------------
# DISPLAY CHAT HISTORY
# ----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ----------------------------
# USER INPUT
# ----------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    # show user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    # ----------------------------
    # GROQ AI RESPONSE
    # ----------------------------
    response = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=st.session_state.messages
)

    ai_reply = response.choices[0].message.content

    # show AI message
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

    with st.chat_message("assistant"):
        st.write(ai_reply)

    # save memory
    save_memory(st.session_state.messages)