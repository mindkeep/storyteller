# storyteller

StoryTeller is a framework for custom narrative rpg games powered by LLMs.
The goal is to allow a person or group of people to play a game where
a game/dungeon master role is simulated via LLM. The hope is to make this
project very modular such that it can be played from the console or over
some more robust chat interface (such as Discord), and connect to different
LLMs (such os OpenAI's Chat-GPT.) The setting and initial prompts will be
set by the user/admin. Everything from there should be a fairly unique
experience.

## plans

* create a basic cli framework that can talk to OpenAI
* create a message history to grow the story
* tokens are limited (and potentially costly), occasionally summarize the
story so far to condense the history into more manageable sizes

## further ideas

* provide game modes with customizable story relevant things to remember
  * skills
  * items
  * player descriptions
  * location
* output complexity stats around tokens and response times
* add a set of commands for Out Of Character operations
  * undo commands
* provide a way to issue pass/fail challenges
  * this could be skill based or percentage based, but likely better to
    solve this outside of the LLM response
