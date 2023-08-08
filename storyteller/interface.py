# provide a generic interface to talk to multiple LLM providers

from enum import Enum
from storyteller.history import History

import openai

# enum for LLM providers
class LLM(Enum):
    DUMMY = 1
    OPENAI = 2
    LLAMA = 3

class Storyteller:
    def __init__(self, model, history_path = None) -> None:
        """Initialize storyteller with a LLM provider"""

        # throw error if model is not a valid LLM provider
        if not isinstance(model, LLM):
            raise ValueError("Invalid LLM provider")
        self._model = model

        # initialize history
        self._history = History(history_path)

    def respond(self, input):
        if not self._model == LLM.DUMMY:
            raise NotImplementedError("Only the dummy model is implemented")
        self._history.add("user", input)
        response = self._dummy_response(input)
        self._history.add("system", response)
        return response

    def _dummy_response(self, input):
        return "No one tells me nuthin..."
    
    def _openai_response(self, input):
        messages = []
        for entry in self._history.get_since_last_summary():
            messages.append({"role": entry.speaker, "text": entry.message})
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=0.5,
            stop=None,
            max_tokens=350)
        return response['choices'][0]['text']  # type: ignore