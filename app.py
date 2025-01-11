import streamlit as st
from datetime import datetime
from chatbot import Chatbot

def main():
    # Set up page configuration
    st.set_page_config(page_title="Bicycle Sales AI Chatbot", layout="wide")

    # Title and welcome message
    st.title("🚴 Bicycle Sales AI Chatbot")
    st.write("Welcome to our bicycle sales chatbot! 🛒 Ask me anything about bicycles.")

    chatbot = Chatbot()

    # Maintain chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Clear chat button
    if st.button("Clear Chat 🗑️"):
        st.session_state.chat_history = []
        st.success("Chat history cleared!")

    # User input section
    with st.form(key='user_input_form'):
        user_input = st.text_input("Type your message here:")
        submit_button = st.form_submit_button(label="Send 🚀")

    # Handle user input and chatbot response
    if submit_button and user_input:
        response = chatbot.get_response(user_input)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.chat_history.append({"role": "user", "text": user_input, "time": timestamp})
        st.session_state.chat_history.append({"role": "assistant", "text": response, "time": timestamp})

    # Display chat history in a scrollable container
    st.write("### Chat History")
    with st.container():
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                st.markdown(f"👤 **You [{chat['time']}]:** {chat['text']}")
            else:
                st.markdown(f"🤖 **Assistant [{chat['time']}]:** {chat['text']}")

if __name__ == "__main__":
    main()
