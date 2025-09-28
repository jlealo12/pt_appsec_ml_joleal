"""Agent script to analyze code againt OWASP top 10"""

import asyncio
import os

from strands import Agent
from strands.models import Model


class OwaspAgent:
    """Base class for OWASP agents."""

    def __init__(
        self,
        model: Model,
        system_prompt: str,
        user_prompt_template: str,
        owasp_name: str,
    ):
        self.agent = Agent(
            model=model,
            system_prompt=system_prompt,
            callback_handler=None,
        )
        self.user_prompt_template = user_prompt_template
        self.owasp_name = owasp_name

    def run_inference(self, code_snippet: str) -> dict:
        """Function to run the agent inference on a given code snippet."""
        # Log action start
        print(f"Starting run for agent: {self.owasp_name}")
        # 1. Format the user inputs
        user_prompt = self.user_prompt_template.format(
            code_snippet=code_snippet,
            owasp_name=self.owasp_name,
        ).strip()
        # Call the inference
        response = self.agent(user_prompt)
        # Process output metrics
        usage_metrics = {
            **response.metrics.accumulated_usage,
            "latencyMs": round(sum(response.metrics.cycle_durations) * 1000, 0),
        }
        # Prepare the payload
        payload = {
            "owasp_name": self.owasp_name,
            "response": str(response),
            "metrics": usage_metrics,
        }
        return payload
