import openai
from dotenv import load_dotenv
import os
from typing import List, Dict, Optional
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
import pkg_resources

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get OpenAI package version
OPENAI_VERSION = pkg_resources.get_distribution('openai').version
IS_NEW_API = int(OPENAI_VERSION.split('.')[0]) >= 1

class ChatbotConfig:
    """Configuration class for the chatbot"""
    def __init__(
        self,
        model: str = "gpt-4-turbo-preview",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        system_message: str = "How can I assist you with bicycle sales today?",
        api_key: Optional[str] = None
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_message = system_message
        # Load environment variables if not already loaded
        load_dotenv()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")

class Chatbot:
    def __init__(self, config: Optional[ChatbotConfig] = None):
        """
        Initialize the chatbot with optional configuration
        
        Args:
            config: ChatbotConfig object with custom settings
        """
        self.config = config or ChatbotConfig()
        
        if IS_NEW_API:
            # For OpenAI package version >= 1.0.0
            from openai import OpenAI
            self.client = OpenAI(api_key=self.config.api_key)
        else:
            # For older versions
            openai.api_key = self.config.api_key
            self.client = openai
            
        self.messages: List[Dict[str, str]] = [
            {"role": "system", "content": self.config.system_message}
        ]
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    def get_response(self, user_input: str) -> str:
        """
        Get a response from the chatbot using the OpenAI API
        
        Args:
            user_input: The user's input message
            
        Returns:
            str: The assistant's response
            
        Raises:
            openai.APIError: If there's an API error
            Exception: For other unexpected errors
        """
        try:
            # Add user message to conversation history
            self.messages.append({"role": "user", "content": user_input})
            
            if IS_NEW_API:
                # For OpenAI package version >= 1.0.0
                response = self.client.chat.completions.create(
                    model=self.config.model,
                    messages=self.messages,
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens
                )
                assistant_reply = response.choices[0].message.content
            else:
                # For older versions
                response = self.client.ChatCompletion.create(
                    model=self.config.model,
                    messages=self.messages,
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens
                )
                assistant_reply = response['choices'][0]['message']['content']
            
            # Store assistant's reply
            self.messages.append({"role": "assistant", "content": assistant_reply})
            
            return assistant_reply
            
        except Exception as e:
            logger.error(f"Error in get_response: {str(e)}")
            raise

    def clear_conversation_history(self) -> None:
        """Reset the conversation history to just the system message"""
        self.messages = [{"role": "system", "content": self.config.system_message}]

    @property
    def conversation_history(self) -> List[Dict[str, str]]:
        """Get the current conversation history"""
        return self.messages.copy()

# Example usage
def main():
    # Create custom configuration
    config = ChatbotConfig(
        model="gpt-4-turbo-preview",
        temperature=0.7,
        max_tokens=1000,
        system_message="I am a bicycle sales specialist. How can I help you today?"
    )
    
    # Initialize chatbot
    chatbot = Chatbot(config)
    
    try:
        # Get response
        response = chatbot.get_response("What's the best mountain bike for beginners?")
        print(f"Assistant: {response}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()