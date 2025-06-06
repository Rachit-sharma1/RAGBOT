import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# === MongoDB Setup ===
MONGO_URI = st.secrets["MONGO_URI"]  # store in .streamlit/secrets.toml
client = MongoClient(MONGO_URI)
db = client["ragbot_db"]
chat_collection = db["chat_history"]

# === Load history from MongoDB ===
def load_user_chat(user_id):
    chat_doc = chat_collection.find_one({"user_id": user_id})
    if chat_doc and "messages" in chat_doc:
        return chat_doc["messages"]
    return []

# === Save one message to MongoDB ===
def save_message(user_id, role, content):
    chat_collection.update_one(
        {"user_id": user_id},
        {"$push": {"messages": {"role": role, "content": content, "timestamp": datetime.utcnow()}}},
        upsert=True
    )

# === Display all messages in chat UI ===
def display_chat_history():
    user_id = st.session_state.get("user", {}).get("email", "guest")
    if "messages" not in st.session_state:
        st.session_state.messages = load_user_chat(user_id)

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

# === Handle user prompt and response ===
def handle_user_input(chain):
    user_id = st.session_state.get("user", {}).get("email", "guest")
    user_input = st.chat_input("Pass your prompt here")
    if not user_input:
        return

    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    save_message(user_id, "user", user_input)

    # Exclude last message (current user input) from chat history
    chat_history = [(m["role"], m["content"]) for m in st.session_state.messages[:-1]]

    try:
        result = chain.invoke({"input": user_input, "chat_history": chat_history})
        response = result["answer"] if "answer" in result else result.get("result", "")
        st.chat_message("assistant").markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        save_message(user_id, "assistant", response)
    except Exception as e:
        st.error(f"Error: {str(e)}")


# === Download chat as text ===
def download_chat_history():
    if st.session_state.get("messages"):
        content = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
        st.download_button("💾 Download Chat History", content, file_name="chat_history.txt", mime="text/plain")
