import openai
from dotenv import load_dotenv
import os
from prompts import get_initial_prompt, get_follow_up_prompt

# Load environment variables from .env file
load_dotenv()

# Ensure API key is loaded correctly
openai.api_key = os.getenv('OPENAI_API_KEY')

if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")


class Chatbot:
    def __init__(self):
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")  # Default to gpt-4 if not set
        self.initial_prompt = get_initial_prompt()
        self.messages = [{"role": "system", "content": self.initial_prompt}]
        self.max_tokens_per_request = 1500  # Adjust as needed for your application

    def _manage_token_limit(self):
        """
        Ensures the total token count in messages doesn't exceed the model's context window.
        Trims older messages if necessary.
        """
        max_context_tokens = 4096 if self.model == "gpt-4" else 2048  # Example token limits

        while len(self.messages) > 1 and sum(len(msg["content"]) for msg in self.messages) > max_context_tokens:
            self.messages.pop(1)  # Remove the oldest user/assistant exchange, keeping system prompt intact

    def get_response(self, customer_input):
        self.messages.append({"role": "user", "content": customer_input})
        self._manage_token_limit()  # Manage token context before sending request

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.messages,
                max_tokens=self.max_tokens_per_request,
                temperature=0.7  # Adjust temperature for response creativity
            )
            assistant_reply = response['choices'][0]['message']['content']
            self.messages.append({"role": "assistant", "content": assistant_reply})
            return assistant_reply
        except openai.error.OpenAIError as e:
            return f"An error occurred: {str(e)}"
