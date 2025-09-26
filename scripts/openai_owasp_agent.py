"""Script to create a base agent with OpenAI integration that validates one of the OWASP top 10 risks."""

from strands import Agent
from strands.models.openai import OpenAIModel
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file


def get_owasp_prompt(risk_code: str) -> str:
    """Retrieve the OWASP prompt for a given risk code."""
    prompt_file = os.path.join(
        os.path.dirname(__file__), "agent_prompts", f"{risk_code}.md"
    )
    with open(prompt_file, "r") as file:
        return file.read()


OWASP_CODE = "A02_CF"  # ["A01_BAC", "A02_CF", "A03_Injection", ""]
OWASP_NAME = "Cryptographic Failures"  # ["Broken Access Control", "Cryptographic Failures", "Injection"]
AGENT_PROMPT = get_owasp_prompt(OWASP_CODE)
USER_PROMPT_TEMPLATE = (
    "Analyze the following code and identify any potential security issues related to {owasp_name}.\n"
    "Provide a detailed explanation of any vulnerabilities found, including how they can be exploited and recommendations for mitigation.\n"
    "Here is the code:\n<code>\n{code_snippet}\n</code>"
)
model = OpenAIModel(
    client_args={
        "api_key": os.getenv("OPENAI_API_KEY"),
    },
    # **model_config
    model_id="gpt-4o",
    params={
        "max_tokens": 800,
        # "max_completion_tokens": 50,
        "temperature": 0.1,
    },
)

# Create an agent using the model
agent = Agent(
    model=model,
    system_prompt=AGENT_PROMPT,
    callback_handler=None,
)

# Use the agent
sample_code_snippet = """import os
def run_command_from_user_input(command):
os.system(f'echo {command}')"""
user_prompt = USER_PROMPT_TEMPLATE.format(
    code_snippet=sample_code_snippet,
    owasp_name=OWASP_NAME,
).strip()
response = agent(user_prompt)

print(str(response))
print(response.metrics)
