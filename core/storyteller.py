"""main module for the storyteller application"""

from langchain.llms import LlamaCpp
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema.messages import ChatMessage

from core import config
from ui.cli import CLIInterface


DEFAULT_SETTING = """
Our adventure begins in a lonely tavern.
The barkeep leans in and says,
"I mean no offense, but you look like you could use some work.
I have a job for you if you're interested."

How do you respond?
"""

PROMPT_TEMPLATE = """You are a dungeon master and responding
to the player's stated actions.

Conversation history:
{memory}

Player response:
{response}

Your response:"""

class StoryTeller:
    """
    Storyteller class
    """
    def __init__(self, conf: config.Config) -> None:
        """
        Initialize the storyteller application
        """

        # store the configuration
        self._conf = conf

        # initialize the chat memory
        self._memory = ConversationBufferMemory(memory_key="memory")
        self._memory.chat_memory.add_message(ChatMessage(role="Setting", content=DEFAULT_SETTING))

        # create our prompt template
        self._prompt_template = PromptTemplate(
            input_variables=["memory", "response"],
            template=PROMPT_TEMPLATE)

        # initialize the callback manager
        if self._conf.interface == config.Interface.CLI:
            self._interface = CLIInterface()
        else:
            raise NotImplementedError(
                f"Interface {self._conf.interface} not implemented."
            )

        # initialize the LLM
        self.set_llm(self._conf.llm_provider)

        # initialize the conversation chain
        self._conversation_chain = LLMChain(
            llm=self._llm,
            prompt=self._prompt_template,
            memory=self._memory)

    def set_llm(self, llm: config.LLMProvider, model: str = "") -> None:
        """
        Set the LLM

        Args:
            llm (config.LLMProvider): the LLM provider
            model (str, optional): the model path. Defaults to "".
        """
         # initialize the LLM
        if llm == config.LLMProvider.LLAMACPP:
            self._llm = LlamaCpp(
                model_path=self._conf.llamacpp_model_path,
                callback_manager=self._interface.get_callback_manager(),
                verbose=True,
            )  # type: ignore
        else:
            raise NotImplementedError(
                f"LLM provider {llm} / model {model} not implemented."
            )

    def run(self) -> None:
        """
        Run the storyteller application
        """
        self._interface.output("Welcome to Storyteller!")
        self._interface.output("Type 'exit' to exit the application.\n")
        self._interface.output(DEFAULT_SETTING)

        while True:
            user_input = self._interface.get_input()
            if user_input in ["exit", "quit"]:
                break
            else:
                response = self._conversation_chain.run(user_input)
                self._interface.output(f"Storyteller: \n{response}")
