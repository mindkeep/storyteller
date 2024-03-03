"""
This module provides the CLI interface
"""

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.schema.messages import ChatMessage

from core import config
from core.storyteller import StoryTeller, PROMPT_TEMPLATE
from core.llamacpp_utils import init_llamacpp, init_chain


class CLI:
    """
    CLI interface class
    """

    def __init__(self, conf: config.Config) -> None:
        """
        Initialize the CLI interface
        """
        self.conf = conf
        self._callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    def run(self) -> None:
        """
        Run the CLI interface
        """

        welcome_str = "Welcome to the StoryTeller CLI!"
        # print the welcome message
        print(welcome_str)
        print('=' * len(welcome_str))

        # initialize the LLM
        if self.conf.llm_provider == config.LLMProvider.LLAMACPP:
            llm = init_llamacpp(self.conf.models[0], self._callback_manager)
        else:
            raise NotImplementedError(
                f"LLM provider {self.conf.llm_provider} not implemented."
            )

        storyteller = StoryTeller(
            llm=llm,
            persona="",
            setting="",
            location="",
        )

        print("Type 'exit' to exit the application.\n")

        msg_history = []
        while True:
            user_input = input("\n\nYou: ")
            if user_input in ["exit", "quit"]:
                break
            else:
                try:
                    llm_out = storyteller.generate_response(
                        msg_history=msg_history,
                        user_input=user_input)
                    msg_history.append({'role': 'user', 'content': user_input})
                    msg_history.append({'role': 'assistant', 'content': llm_out})
                except Exception as err:  # pylint: disable=broad-except
                    print(f"Error: {err}")
                    continue
