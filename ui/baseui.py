"""
This module contains the base interface class
"""

from abc import ABC, abstractmethod
from core import config

class BaseUI(ABC):
    """
    Interface class
    """

    def __init__(self, conf: config.Config) -> None:
        """
        Initialize the interface
        """
        self.conf = conf

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
    async def get_input(self) -> str:
        """
        Get input from the interface
        """

    @abstractmethod
    def get_callback_manager(self) -> None:
        """
        Get the callback manager
        """
