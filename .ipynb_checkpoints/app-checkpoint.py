import streamlit as st
from chatbot import Chatbot

def main():
    st.title("Bicycle Sales AI Chatbot")
    st.write("Welcome to our bicycle sales chatbot! Ask me anything about bicycles.")

    chatbot = Chatbot()

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("You: ")

    if st.button("Send"):
        if user_input:
            response = chatbot.get_response(user_input)
            st.session_state.chat_history.append({"user": user_input, "assistant": response})

    if st.session_state.chat_history:
        for chat in st.session_state.chat_history:
            st.write(f"You: {chat['user']}")
            st.write(f"Assistant: {chat['assistant']}")

if __name__ == "__main__":
    main()
