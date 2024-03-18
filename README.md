# storyteller

StoryTeller is a framework for custom narrative rpg games powered by LLMs.
The goal is to allow a person or group of people to play a game where
a game/dungeon master role is simulated via LLM. We're going to use OpenAI's
API for now. (llama_cpp_python's server module works well as a testing
replacement.) The setting and initial prompts will be set by the user/admin.
Everything from there should be a fairly unique experience that can be saved
and continued later. Scenarios can be left very open ended and allow the AI
to fill in the gaps, or they can be very specific with large user entered
context and rules.

## plans

* multi-game support and saving
* interfaces
  * cli
  * flet - making a flet (flutter) interface
  * discord
* LLMS
  * switching to aim primarily at OpenAI's API since there are a lot of
    compatibility options available.
* multiplayer support and joining games (easiest as a discord bot probably)
* allow history and memory to be edited.
* manage specific game states apart from chat history to better represent a
  persistent world.
  * At first this will only be a running Summary to manage the context window
    of smaller LLMs (or limit token usage of larger ones).
* move history and game states/summaries into a database (likely mongodb as I've used it before).
