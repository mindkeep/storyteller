"""
This module provides the CLI interface
"""

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from ui.common import Interface

class CLIInterface(Interface):
    """
    CLI interface class
    """

    def __init__(self) -> None:
        """
        Initialize the CLI interface
        """
        super().__init__()
        self._callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    def output(self, text: str) -> None:
        """
        Output text to the interface
        """
        print(text)

    def get_input(self) -> str:
        """
        Get input from the interface
        """
        return input("You: ")

    def get_callback_manager(self) -> CallbackManager:
        """
        Get the callback manager
        """
        return self._callback_manager
