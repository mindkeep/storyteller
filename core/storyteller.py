"""main module for the storyteller application"""

from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.llms.base import LLM


PROMPT_TEMPLATE = """{persona}

Example interaction:
AI: You enter the tavern and sees a barkeep and a few adventures whispering
to each other over drinks at a round table.
Human: I walk over to the table ask if I can join them.
AI: They look you up and down and decide to ignore you and continue their
conversation. Behind you, you hear the barkeep laugh.

Settings: {setting}

Current location: {location}

Conversation history:
{memory}

Human: {user_input}
AI: """


class StoryTeller:
    """
    Storyteller class
    """

    def __init__(
        self, llm: LLM, persona: str, setting: str, location: str
    ) -> None:
        """
        Initialize the storyteller application
        """
        self.llm = llm
        self.persona = persona
        self.setting = setting
        self.location = location

    def generate_response(
        self,
        msg_history: ConversationBufferMemory,
        user_input: str
    ) -> str:
        """
        Generate a response to the given input
        """
        prompt = PromptTemplate.from_template(template=PROMPT_TEMPLATE)
        
        chain = prompt | self.llm
 
        return chain.invoke(
            input={
                'user_input': user_input,
                'persona': self.persona,
                'setting': self.setting,
                'location': self.location,
                'memory': msg_history
                })
