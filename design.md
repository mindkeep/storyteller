# design ideas


One of the ideas in this is to have the Storyteller take into account the attitude of the player and work with (or against) them based on how well intentioned they are. Basically I want to make the Storyteller a bit of a jerk if the player is a jerk.

Creative prompt building will be the key in this project. How do we give the LLM the right context to continue an interaction while supplying the most relevant history?

Does the character have the skills and equipment to pull off whatever the player is asking? Even if they don't, maybe it's a calculated risk to learn the skill if successful. There are tons of possibilities here, but of course, each question is potentially a new prompt and a new response, and costs resources/time.

```mermaid
flowchart TD
    start[Start] --> input[Input]
    input -->|What is the player trying to do?| redirect{LLM\nRedirect}
    redirect -->|Ask for clarity| clarify[Clarify]
    clarify -->|Clarify previous response| input
    redirect -->|Take some game action| action[Game Action]
    action -->|Does this make sense?| sanity{LLM\nSanity Check}
    sanity -->|Yes| attempt[Attempt the action]
    sanity -->|No| guidance[Give the player some guidance]
    guidance -->|revert and ask for input| input
    guidance -->|Do it anyway!| attempt
    attempt -->|FAFO| response[Response]
    response --> update[LLM\nUpdate the game state]
    update --> input
    
```


# saved ideas
This is older stuff that I'm not sure if I want to keep or not. I'm keeping it here for now.

Currently I'm stepping away from this in favor of MemGPT.

Diagram around the design of the project. This is a work in progress.

class diagram
```mermaid
classDiagram
    Description --* GameState
    Summary --* GameState
    HistEntry --* GameState

    Storyteller --* GameState
    Player --* Character
    Character --* GameState
    class Summary {
        + datetime date
        + GameTime game_date
        + string summary
        + float[] embedding
    }
    class Description {
        + datetime date
        + string description
        + float[] embedding
    }
    class HistEntry {
        + datetime date
        + string input
        + string response
        + float[] embedding
    }
    class GameState {
        + string name
        + string description
        + string location
        + GameTime game_date
        + Summary[] summaries
        + Description[] descriptions
        + HistEntry[] history
    }
    class GameTime {
        + int year
        + int month
        + int day
        + int hour
        + int minute
        + int second
    }
    class Storyteller {
        string model
        string description
        string attitude
        string 
    }
    class Player {
        + string name
        + string description
        + int advantages
        + string attitude
    }
    class Character {
        + string name
        + string description
        + string location
        + string[] inventory
        + string[] skills
        + string[] traits
        + string[] relationships
        + string[] goals
        + string[] secrets
        + string[] history
    }
```