"""Script used to handle configurations for the project"""

from dataclasses import dataclass

from .utils import get_env_variable

# Constants
USER_PROMPT_TEMPLATE = (
    "Analyze the following code and identify any potential security issues related to {owasp_name}.\n"
    "Provide a detailed explanation of any vulnerabilities found, including how they can be exploited and recommendations for mitigation.\n"
    "Here is the code:\n<code>\n{code_snippet}\n</code>"
)


# Data models
@dataclass
class OpenAIModelConfig:
    """Dataclass to hold model configuration details."""

    model_id: str
    params: dict
    client_args: dict

    @classmethod
    def from_dict(cls, config: dict):
        return cls(
            model_id=config.get("model_id", "gpt-4o"),
            params=config.get("params", {"max_tokens": 800, "temperature": 0.1}),
            client_args=config.get(
                "client_args", {"api_key": get_env_variable("OPENAI_API_KEY")}
            ),
        )

    def to_dict(self) -> dict:
        return {
            "model_id": self.model_id,
            "params": self.params,
            "client_args": self.client_args,
        }
