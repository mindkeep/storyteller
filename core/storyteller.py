"""main module for the storyteller application"""

from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain

DEFAULT_SETTING = """Our adventure begins in a lonely tavern. The barkeep
leans in and says, "I mean no offense, but you look like you could use some
work. I have a job for you if you're interested." """

PROMPT_TEMPLATE = """You are a dungeon master and responding
to the player's stated actions.

Example interaction:
AI: You enter the tavern and sees a barkeep and a few adventures whispering
to each other over drinks at a round table.
Human: I walk over to the table ask if I can join them.
AI: They look you up and down and decide to ignore you and continue their
conversation. Behind you, you hear the barkeep laugh.

Conversation history:
{memory}
Human: {response}
AI: """

class StoryTeller():
    """
    Storyteller class
    """

    def __init__(
            self,
            llm_chain: LLMChain,
            memory: ConversationBufferMemory) -> None:
        """
        Initialize the storyteller application
        """
        self.llm_chain = llm_chain
        self.memory = memory
