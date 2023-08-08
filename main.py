# main entry point to have a dialogue with the user and ChatGPT

import openai
import yaml

from storyteller import Storyteller, LLM

default_setting = """
Our adventure begins in a lonely tavern.
The barkeep leans in and says,
"I mean no offense, but you look like you could use some work.
I have a job for you if you're interested."

How do you respond?
"""

system_prompt = "You are a dungeon master and responding to the player's stated actions."

def init():
    # Load config
    with open("config.yml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    openai.api_key = config["openai_key"]

def run():
    """ Run the main loop."""
    
    st = Storyteller(LLM.DUMMY)
    
    print(default_setting)
        
    while True:
        print()
        user_input = input(">> ")
        if user_input == 'exit' or user_input == 'quit':
            break
        response = st.respond(user_input)

        print(response)

if __name__ == "__main__":
    init()
    run()
