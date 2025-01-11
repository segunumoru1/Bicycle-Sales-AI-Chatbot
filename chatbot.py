import openai
from dotenv import load_dotenv
import os
from prompts import get_initial_prompt, get_follow_up_prompt

# Load environment variables from .env file
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

class Chatbot:
    def __init__(self):
        self.initial_prompt = get_initial_prompt()
        self.messages = [{"role": "system", "content": self.initial_prompt}]

    def get_response(self, customer_input):
        self.messages.append({"role": "user", "content": customer_input})
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=self.messages
        )
        assistant_reply = response['choices'][0]['message']['content']
        self.messages.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply
