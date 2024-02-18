"""
This module provides the CLI interface
"""

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.schema.messages import ChatMessage

from core import config
from core.storyteller import StoryTeller, DEFAULT_SETTING
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

        # print the welcome message
        print("Welcome to the StoryTeller CLI!")

        # prompt the user for a session name
        session_name = input("Enter a session name: ")
        print(f"Session name: {session_name}")

        # if the session is not found, ask if a new session should be created
        # TODO: implement this

        # create the storyteller memory
        # TODO: implement new and load memory functions
        memory = ConversationBufferMemory(memory_key="memory")
        memory.chat_memory.add_message(
            ChatMessage(role="Setting", content=DEFAULT_SETTING)
        )

        # initialize the LLM
        if self.conf.llm_provider == config.LLMProvider.LLAMACPP:
            llm = init_llamacpp(self.conf.models[0], self._callback_manager)
        else:
            raise NotImplementedError(
                f"LLM provider {self.conf.llm_provider} not implemented."
            )

        storyteller = StoryTeller(
            llm_chain=init_chain(
                llm=llm, memory=memory, cb_manager=self._callback_manager
            ),
            memory=memory,
        )

        print("Type 'exit' to exit the application.\n")

        while True:
            user_input = input("\n\nYou: ")
            if user_input in ["exit", "quit"]:
                break
            else:
                try:
                    storyteller.llm_chain.run(user_input)
                except Exception as err:  # pylint: disable=broad-except
                    print(f"Error: {err}")
                    continue
