"""Script to create a base agent with OpenAI integration."""

import os
from typing import List, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from strands import Agent
from strands.models.openai import OpenAIModel

load_dotenv()  # Load environment variables from .env file


class ValidationResult(BaseModel):
    """Model for structured validation results."""

    vulnerabilities_detected: List[str] = Field(
        default_factory=list,
        description="List of detected vulnerabilities in the code snippet.",
    )
    recommendations: Optional[str] = Field(
        None,
        description="Recommendations for mitigating the detected vulnerabilities.",
    )


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
agent = Agent(
    model=model,
    # system_prompt=AGENT_PROMPT,
    callback_handler=None,
)

# Use the agent
analysis_result = """Risk: Injection (A03)
```yaml
vulnerabilities_detected:
  - file: [provided_code]
    line: 3
    type: OS Command Injection
    description: |
        The function `run_command_from_user_input` takes a user-supplied input `command` and directly interpolates it into a shell command using `os.system`. This allows an attacker to inject arbitrary shell commands. For example, if an attacker provides a command like `"; rm -rf /"`, it would execute the `rm -rf /` command, potentially deleting all files on the system.
    suggested_fix: |
      To mitigate this vulnerability, avoid using `os.system` with user input. Instead, use the `subprocess` module with a list of arguments to safely execute commands. For example:

      ```python
      import subprocess

      def run_command_from_user_input(command):
          # Split the command into a list of arguments
          args = command.split()
          # Use subprocess.run with a list of arguments to avoid shell injection
          subprocess.run(args, check=True)
      ```

      Additionally, validate and sanitize the input to ensure it only contains expected commands and arguments. Consider using an allowlist of permissible commands.  
```"""
user_prompt = f"{analysis_result}"
result = agent.structured_output(
    ValidationResult,
    user_prompt,
)
print(result.model_dump_json(indent=2))
