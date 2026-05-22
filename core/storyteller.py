"""Main module for the StoryTeller LLM interface."""

import os
from typing import List, Dict, Iterable
from openai import OpenAI

HISTORY_LIMIT = 20

PROMPT_TEMPLATE = """{persona}

Setting: {setting}

Current location: {location}

--- GAME NOTES ---
{notes}
--- END NOTES ---

Respond only as the dungeon master. Continue the narrative from the player's action."""

NOTES_UPDATE_TEMPLATE = """You are a record-keeper for a narrative RPG. Update the game notes to reflect \
current state. Keep it under 200 words. Cover: current location, active goals or quests, key NPCs \
encountered, notable items or events, plot threads in progress. Write in present tense. Replace the \
old notes entirely.

PREVIOUS NOTES:
{old_notes}

RECENT EXCHANGE:
Player: {user_input}
Narrator: {assistant_response}

Updated notes:"""


class StoryTeller:
    def __init__(self, persona: str, setting: str, location: str) -> None:
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
        )
        self.persona = persona
        self.setting = setting
        self.location = location

    def _build_messages(
        self, msg_history: List[Dict[str, str]], user_input: str, notes: str = ""
    ) -> List[Dict[str, str]]:
        system_prompt = PROMPT_TEMPLATE.format(
            persona=self.persona,
            setting=self.setting,
            location=self.location,
            notes=notes,
        )
        return (
            [{"role": "system", "content": system_prompt}]
            + msg_history
            + [{"role": "user", "content": user_input}]
        )

    def get_response(
        self, msg_history: List[Dict[str, str]], user_input: str, notes: str = ""
    ) -> str:
        messages = self._build_messages(msg_history, user_input, notes)
        response = self.client.chat.completions.create(
            model=os.getenv("OPENAI_API_MODEL"), messages=messages
        )
        return response.choices[0].message.content

    def get_stream_response(
        self, msg_history: List[Dict[str, str]], user_input: str, notes: str = ""
    ) -> Iterable[str]:
        messages = self._build_messages(msg_history, user_input, notes)
        response = self.client.chat.completions.create(
            model=os.getenv("OPENAI_API_MODEL"),
            messages=messages,
            stream=True,
        )
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content is None:
                continue
            yield content

    def get_notes_update(
        self, old_notes: str, user_input: str, assistant_response: str
    ) -> str:
        prompt = NOTES_UPDATE_TEMPLATE.format(
            old_notes=old_notes or "(none yet)",
            user_input=user_input,
            assistant_response=assistant_response,
        )
        response = self.client.chat.completions.create(
            model=os.getenv("OPENAI_API_MODEL"),
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()
