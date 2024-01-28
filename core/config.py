""" This module handles the configuration of storyteller application. """

from enum import Enum
from typing import List

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
    GUI = "gui"
    WEB = "web"

class LlamaCppModel(BaseModel):
    """
    Configuration class for LlamaCpp model
    """

    name: str
    path: str
    n_ctx: int
    temperature: float

class Config(BaseModel):
    """
    Configuration class for storyteller application
    """

    llm_provider: LLMProvider
    openai_key: str
    openai_model: str
    ui: UI
    models: List[LlamaCppModel]


def load_config(path: str = "config.yml") -> Config:
    """
    Loads the configuration file
    """
    with open(file=path, mode="r", encoding="utf-8") as file:
        return Config(**yaml.safe_load(file))
