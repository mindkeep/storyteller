"""
This module provides the CLI interface
"""

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from ui.baseui import BaseUI
from core.config import Config
from core.storyteller import StoryTeller

class CLI(BaseUI):
    """
    CLI interface class
    """

    def __init__(self, conf: Config) -> None:
        """
        Initialize the CLI interface
        """
        super().__init__(conf)
        self._callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    def run(self) -> None:
        """
        Run the CLI interface
        """

        # print the welcome message
        self.output("Welcome to the StoryTeller CLI!")

        storyteller = StoryTeller(self._conf, self)
        storyteller.run()

    def output(self, text: str) -> None:
        """
        Output text to the interface
        """
        print(text)

    def get_input(self) -> str:
        """
        Get input from the interface
        """
        return input("\n\nYou: ")

    def get_callback_manager(self) -> CallbackManager:
        """
        Get the callback manager
        """
        return self._callback_manager
