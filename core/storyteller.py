import os
from typing import List, Dict
from openai import OpenAI

"""main module for the storyteller application"""

PROMPT_TEMPLATE = """{persona}

Example interaction:
AI: You enter the tavern and sees a barkeep and a few adventures whispering
to each other over drinks at a round table.
Human: I walk over to the table ask if I can join them.
AI: They look you up and down and decide to ignore you and continue their
conversation. Behind you, you hear the barkeep laugh.

Settings: {setting}

Current location: {location}
"""


class StoryTeller:
    """
    Storyteller class
    """

    def __init__(self, persona: str, setting: str, location: str) -> None:
        """
        Initialize the storyteller application
        """
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE"),
        )
        self.persona = persona
        self.setting = setting
        self.location = location

    def generate_response(
        self, msg_history: List[Dict[str, str]], user_input: str
    ) -> str:
        """
        Generate a response to the given input
        """
        system_prompt = PROMPT_TEMPLATE.format(
            persona=self.persona, setting=self.setting, location=self.location
        )

        # prepend the system prompt to the message history and
        # append the user input
        messages = (
            [{"role": "system", "content": system_prompt}]
            + msg_history
            + [{"role": "user", "content": user_input}]
        )

        response = self.client.chat.completions.create(
            model=os.getenv("OPENAI_API_MODEL"), messages=messages
        )

        return response.choices[0].message.content
