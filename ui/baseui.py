"""
This module contains the base interface class
"""

from abc import ABC, abstractmethod
from core.config import Config

class BaseUI(ABC):
    """
    Interface class
    """

    def __init__(self, conf: Config) -> None:
        """
        Initialize the interface
        """
        self._conf = conf

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
