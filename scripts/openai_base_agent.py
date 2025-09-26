"""Script to create a base agent with OpenAI integration."""

from strands import Agent
from strands.models.openai import OpenAIModel
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file


model = OpenAIModel(
    client_args={
        "api_key": os.getenv("OPENAI_API_KEY"),
    },
    # **model_config
    model_id="gpt-4o",
    params={
        "max_tokens": 100,
        # "max_completion_tokens": 50,
        "temperature": 0.1,
    },
)

# Create an agent using the model
agent = Agent(model=model)

# Use the agent
agent("Tell me about Strands agents.")  # Prints model output to stdout by default
