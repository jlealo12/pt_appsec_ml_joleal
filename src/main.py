"""main entrypoint for testing"""

import asyncio
import json
import os

from dotenv import load_dotenv
from .utils import get_env_variable
from .workflow import OwaspWorkflow

load_dotenv()  # Load environment variables from .env file


def pprint(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    CONFIG_PATH = os.path.join(
        os.path.dirname(__file__),
        get_env_variable("CONFIG_PATH"),
    )
    workflow = OwaspWorkflow(CONFIG_PATH)
    sample_code_snippet = """import os
    def run_command_from_user_input(command):
    os.system(f'echo {command}')"""

    result = asyncio.run(workflow.run_async_inference(sample_code_snippet))
    pprint(result)
