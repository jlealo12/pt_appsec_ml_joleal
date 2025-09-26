"""Script to create a base agent with Ollama integration."""

from strands import Agent
from strands.models.ollama import OllamaModel

# Create an Ollama model instance
ollama_model = OllamaModel(
    host="http://localhost:11434",  # Ollama server address
    model_id="gemma3:1b",  # Specify which model to use
)

# Create an agent using the Ollama model
agent = Agent(model=ollama_model)

# Use the agent
agent("Tell me about Strands agents.")  # Prints model output to stdout by default
