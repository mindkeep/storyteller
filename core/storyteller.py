"""main module for the storyteller application"""

from langchain.llms import LlamaCpp

# from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from core import config

# from storyteller import Storyteller, LLM

DEFAULT_SETTING = """
Our adventure begins in a lonely tavern.
The barkeep leans in and says,
"I mean no offense, but you look like you could use some work.
I have a job for you if you're interested."

How do you respond?
"""

SYSTEM_PROMPT = (
    "You are a dungeon master and responding to the player's stated actions."
)

class StoryTeller:
    """
    Storyteller class
    """
    def __init__(self, conf: config.Config) -> None:
        """
        Initialize the storyteller application
        """
        self._conf = conf
        self._callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        self._llm = LlamaCpp(
            model_path=conf.llamacpp_model_path,
            callback_manager=self._callback_manager,
            verbose=True,
        )  # type: ignore

    def run(self) -> None:
        """
        Run the storyteller application
        """
        print("Welcome to Storyteller!")
        print("Type 'exit' to exit the application.")
        print()

        while True:
            user_input = input("You: ")
            if user_input in ["exit", "quit"]:
                break
            else:
                response = self._llm(user_input)
                print(f"Storyteller: \n{response}")
