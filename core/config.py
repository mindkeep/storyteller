""" This module handles the configuration of storyteller application. """

from enum import Enum

from pydantic import BaseModel  # pylint: disable=no-name-in-module

import yaml


class LLMProvider(str, Enum):
    """
    Enum class for LLM provider
    """

    LLAMACPP = "llamacpp"
    OPENAI = "openai"


class UI(str, Enum):
    """
    Enum class for Interface
    """

    CLI = "cli"
    WEB = "web"


class Config(BaseModel):
    """
    Configuration class for storyteller application
    """

    llm_provider: LLMProvider
    openai_key: str
    openai_model: str
    llamacpp_model_path: str
    ui: UI


def load_config(path: str = "config.yml") -> Config:
    """
    Loads the configuration file
    """
    with open(file=path, mode="r", encoding="utf-8") as file:
        return Config(**yaml.safe_load(file))
