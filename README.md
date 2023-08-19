# storyteller

StoryTeller is a framework for custom narrative rpg games powered by LLMs.
The goal is to allow a person or group of people to play a game where
a game/dungeon master role is simulated via LLM. The hope is to make this
project very modular such that it can be played from the console or over
some more robust chat interface (such as Discord), and connect to different
LLMs (such as OpenAI's Chat-GPT or Llama-2.) The setting and initial prompts
will be set by the user/admin. Everything from there should be a fairly unique
experience.

## plans

* multi-game support and saving
* interfaces
  * maybe a better managed cli
  * discord
  * streamlit or streamsync
* LLMS
  * add OpenAI back as an LLM
  * make LLamaCpp a singleton instance (or microservice)
* multiplayer support and joining games (easiest as a discord bot probably)
* Langchain and different game modes
  * Free form chat mode (basically what we have now)
  * Item tracking
  * Skills checking and challenges
    * via LangChain tools
  * More prompt templates,
* output complexity stats around tokens and response times
* add a set of commands for Out Of Character operations
  * undo commands
  * history edits and tweaks?
