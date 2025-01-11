import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class Chatbot:
    def __init__(self):
        self.model = "gpt-4"
        self.messages = [{"role": "system", "content": "How can I assist you with bicycle sales today?"}]

    def get_response(self, user_input):
        self.messages.append({"role": "user", "content": user_input})
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.messages,
                temperature=0.7
            )
            assistant_reply = response['choices'][0]['message']['content']
            self.messages.append({"role": "assistant", "content": assistant_reply})
            return assistant_reply
        except openai.error.OpenAIError as e:
            return f"Error fetching response: {e}"
