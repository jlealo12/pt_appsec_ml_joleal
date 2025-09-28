"""Utilities used for the project."""

import json
import os


def get_env_variable(var_name: str) -> str:
    """Get an environment variable or raise an error if not found."""
    value = os.getenv(var_name)
    if value is None:
        raise EnvironmentError(f"Environment variable {var_name} not found.")
    return value


def load_json_config(file_path: str) -> dict:
    """Load a JSON configuration file."""
    with open(file_path, "r") as file:
        return json.load(file)


def load_markdown_file(file_path: str) -> str:
    """Load a markdown file and return its content as a string."""
    with open(file_path, "r") as file:
        return file.read()
