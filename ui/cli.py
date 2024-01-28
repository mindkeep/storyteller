"""
This module provides the CLI interface
"""

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.schema.messages import ChatMessage

from ui.baseui import BaseUI
from core import config
from core.storyteller import StoryTeller, DEFAULT_SETTING
from core.llamacpp_utils import init_llamacpp, init_chain

class CLI(BaseUI):
    """
    CLI interface class
    """

    def __init__(self, conf: config.Config) -> None:
        """
        Initialize the CLI interface
        """
        super().__init__(conf=conf)
        self._callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    def run(self) -> None:
        """
        Run the CLI interface
        """

        # print the welcome message
        self.output("Welcome to the StoryTeller CLI!")

        # prompt the user for a session name
        session_name = input("Enter a session name: ")
        print(f"Session name: {session_name}")

        # if the session is not found, ask if a new session should be created
        #TODO: implement this

        # create the storyteller memory
        #TODO: implement new and load memory functions
        memory = ConversationBufferMemory(memory_key="memory")
        memory.chat_memory.add_message(ChatMessage(role="Setting", content=DEFAULT_SETTING))

        # initialize the LLM
        if self.conf.llm_provider == config.LLMProvider.LLAMACPP:
            llm = init_llamacpp(self.conf.models[0], self)
        else:
            raise NotImplementedError(
                f"LLM provider {self.conf.llm_provider} not implemented."
            )

        storyteller = StoryTeller(
            ui=self,
            llm_chain=init_chain(llm=llm, interface=self, memory=memory),
            memory=memory,
        )
        storyteller.run()

    def output(self, text: str) -> None:
        """
        Output text to the interface
        """
        print(text)

    async def get_input(self) -> str:
        """
        Get input from the interface
        """
        return await input("\n\nYou: ")

    def get_callback_manager(self) -> CallbackManager:
        """
        Get the callback manager
        """
        return self._callback_manager
