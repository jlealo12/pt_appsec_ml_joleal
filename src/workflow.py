"""Script used to orchestrate the inference workflow"""

import asyncio
import os

from strands.models.openai import OpenAIModel

from .agent import OwaspAgent
from .config import USER_PROMPT_TEMPLATE, OpenAIModelConfig
from .utils import load_json_config, load_markdown_file


class OwaspWorkflow:
    """Class to handle the OWASP analysis workflow."""

    def __init__(self, evaluation_config_path: str):
        self.evaluation_config = load_json_config(evaluation_config_path)
        self.agents = self._initialize_agents()

    def _initialize_agents(self) -> dict:
        """Initialize agents for each OWASP rule defined in the evaluation configuration."""
        agents = {}
        for owasp_id, details in self.evaluation_config["rules"].items():
            owasp_name = details["name"]
            system_prompt = load_markdown_file(
                os.path.join(
                    os.path.dirname(__file__),
                    details.get("prompt_path"),
                )
            )
            model_config = OpenAIModelConfig.from_dict(details.get("model_config", {}))
            model = OpenAIModel(**model_config.to_dict())
            agents[owasp_id] = OwaspAgent(
                model=model,
                system_prompt=system_prompt,
                user_prompt_template=USER_PROMPT_TEMPLATE,
                owasp_name=owasp_name,
            )
        return agents

    def run_inference(self, code_snippet: str) -> list:
        """Run inference for all OWASP rules on the provided code snippet."""
        results = []
        for owasp_id, agent in self.agents.items():
            print(f"Running agent for {owasp_id}")
            response = agent.run_inference(code_snippet)
            results.append(response)
        return results

    async def run_async_inference(self, code_snippet: str) -> list:
        """Asynchronous execution to run multiple inferences concurrently."""
        loop = asyncio.get_running_loop()
        tasks = [
            loop.run_in_executor(None, agent.run_inference, code_snippet)
            for agent in self.agents.values()
        ]
        results = await asyncio.gather(*tasks)
        # Flatten the list of results
        # return [item for sublist in results for item in sublist]
        return results
