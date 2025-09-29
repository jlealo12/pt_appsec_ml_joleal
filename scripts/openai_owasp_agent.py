"""Script to create a base agent with OpenAI integration that validates one of the OWASP top 10 risks."""

from strands import Agent
from strands.models.openai import OpenAIModel

import asyncio
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


EVALUATION_CONFIG = {
    "rules": {
        "A01_BAC": {"name": "Broken Access Control"},
        "A02_CF": {"name": "Cryptographic Failures"},
        "A03_Injection": {"name": "Injection"},
    }
}
OWASP_CODE = "A02_CF"  # ["A01_BAC", "A02_CF", "A03_Injection", ""]
OWASP_NAME = "Cryptographic Failures"  # ["Broken Access Control", "Cryptographic Failures", "Injection"]
AGENT_PROMPT = get_owasp_prompt(OWASP_CODE)
USER_PROMPT_TEMPLATE = (
    "Analyze the following code and identify any potential security issues related to {owasp_name}.\n"
    "Provide a detailed explanation of any vulnerabilities found, including how they can be exploited and recommendations for mitigation.\n"
    "Here is the code:\n<code>\n{code_snippet}\n</code>"
)
MODEL = OpenAIModel(
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


def run_agent_inference(code_snippet: str, owasp_id: str, owasp_name: str) -> dict:
    """Function to run the agent inference on a given code snippet."""
    print(f"Running agent for {owasp_id}")
    agent_prompt = get_owasp_prompt(owasp_id)
    ############### Model configuration can be adjusted here if needed #################

    # Create an agent using the model
    agent = Agent(
        model=MODEL,
        system_prompt=agent_prompt,
        callback_handler=None,
    )
    user_prompt = USER_PROMPT_TEMPLATE.format(
        code_snippet=code_snippet,
        owasp_name=owasp_name,
    ).strip()
    response = agent(user_prompt)
    usage_metrics = {
        **response.metrics.accumulated_usage,
        "latencyMs": round(sum(response.metrics.cycle_durations) * 1000, 0),
    }
    payload = {
        "owasp_name": owasp_name,
        "response": str(response),
        "metrics": usage_metrics,
    }
    return payload


# Use the agent
sample_code_snippet = """import os
def run_command_from_user_input(command):
os.system(f'echo {command}')"""

# for rule_key, rule_info in EVALUATION_CONFIG["rules"].items():
#     print(f"Running agent for {rule_key} - {rule_info['name']}")
#     result = run_agent_inference(
#         code_snippet=sample_code_snippet,
#         owasp_id=rule_key,
#         owasp_name=rule_info["name"],
#     )
#     print(result)


# Asynchronous execution to run multiple inferences concurrently
async def run_all_inference():
    loop = asyncio.get_running_loop()
    tasks = [
        asyncio.to_thread(
            run_agent_inference,
            code_snippet=sample_code_snippet,
            owasp_id=rule_key,
            owasp_name=rule_info["name"],
        )
        for rule_key, rule_info in EVALUATION_CONFIG["rules"].items()
    ]
    results = await asyncio.gather(*tasks)
    return results


results = asyncio.run(run_all_inference())
for result in results:
    print(f"Results for rule: {result['owasp_name']}\n")
    print(result["response"])
    print("\n" + "=" * 80 + "\n")
