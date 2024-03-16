# storyteller

StoryTeller is a framework for custom narrative rpg games powered by LLMs.
The goal is to allow a person or group of people to play a game where
a game/dungeon master role is simulated via LLM. The hope is to make this
project very modular such that it can be played from the console or over
some more robust chat interface (such as Discord), and connect to different
LLMs (such as OpenAI's Chat-GPT or Llama-2.) The setting and initial prompts
will be set by the user/admin. Everything from there should be a fairly unique
experience that can be saved and continued later. Scenarios can be left very
open ended and allow the AI to fill in the gaps, or they can be very specific
with large user entered context and rules.

## plans

* multi-game support and saving
* interfaces
  * cli
  * flet - making a flet (flutter) interface
  * discord
* LLMS
  * switching to aim primarily at OpenAI's API since there are a lot of compatibility
    options available
* MemGPT
  * Ultimately I'd like to track some specific things manually. However,
    MemGPT is a great starting point and may even become the long term solution
    with some additional function calls.
* multiplayer support and joining games (easiest as a discord bot probably)
* allow history and memory to be edited
