"""
This module contains the base interface class
"""

from abc import ABC, abstractmethod
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from core import config

class BaseUI(BaseModel, ABC):
    """
    Interface class
    """

    conf: config.Config

    @abstractmethod
    def run(self) -> None:
        """
        Run the interface
        """

    @abstractmethod
    def output(self, text: str) -> None:
        """
        Output text to the interface
        """

    @abstractmethod
    def get_input(self) -> str:
        """
        Get input from the interface
        """

    @abstractmethod
    def get_callback_manager(self) -> None:
        """
        Get the callback manager
        """
