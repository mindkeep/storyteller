# main entry point to have a dialogue with the user and ChatGPT

from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

import yaml

#from storyteller import Storyteller, LLM

default_setting = """
Our adventure begins in a lonely tavern.
The barkeep leans in and says,
"I mean no offense, but you look like you could use some work.
I have a job for you if you're interested."

How do you respond?
"""

system_prompt = "You are a dungeon master and responding to the player's stated actions."

# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
# Verbose is required to pass to the callback manager

# Make sure the model path is correct for your system!
llm = LlamaCpp(
    model_path="/home/dave/Downloads/llama-2-7b-chat.ggmlv3.q4_K_M.bin",
    #input={"temperature": 0.75, "max_length": 2000, "top_p": 1},
    callback_manager=callback_manager,
    verbose=True,
)

if __name__ == "__main__":
    response = llm(default_setting)