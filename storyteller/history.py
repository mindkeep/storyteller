""" Class for the history of the game.
"""

import yaml

class Event:
    """
    An event in the history of the game.
    """
    def __init__(self, message, speaker):
        self.message = message
        self.speaker = speaker


class History:
    """ History of the game.
    """
    def __init__(self, path = None):
        """ Initialize the history.
        """

        if path is not None:
            self._path = path
            self._load()
        else:
            self._path = None
            self._history = []

        self._last_summary_index = 0
        
    def _load(self):
        pass

    def add(self, speaker, message):
        """ Add an event to the history.
        """
        self._history.append(Event(message, speaker))
        
    def get_since_last_summary(self):
        return self._history[self._last_summary_index:]

    def __str__(self):
        return "\n".join([str(event) for event in self._history])