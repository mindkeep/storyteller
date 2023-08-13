"""main entry point to have a dialogue with the user and an LLM"""

from core.storyteller import StoryTeller
from core import config

if __name__ == "__main__":
    st = StoryTeller(config.load_config(path="config.yml"))
    st.run()
