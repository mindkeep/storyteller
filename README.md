# StoryTeller

A single-player narrative RPG where an LLM acts as your dungeon master. You type free-form actions; the AI narrates what happens. Games are saved between sessions and the DM maintains running notes on plot, location, and goals so it never loses the thread.

Works with any OpenAI-compatible API — including local models via [Ollama](https://ollama.com) or llama.cpp.

---

## Setup

**Requirements:** Python 3.14+, [uv](https://docs.astral.sh/uv/)

```bash
git clone <repo>
cd storyteller
uv sync
cp .env.template .env
# edit .env with your API key and model
```

**.env variables:**

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | API key (`sk-nothing` works for local servers) |
| `OPENAI_BASE_URL` | Endpoint — use `https://api.openai.com/v1` for OpenAI, or your local server URL |
| `OPENAI_API_MODEL` | Model name, e.g. `gpt-4o-mini` or `gemma4:e4b` |

---

## Running

```bash
# Desktop app (Flet GUI)
uv run python main.py --gui

# Terminal (CLI)
uv run python main.py
```

---

## CLI commands

Once launched, use slash commands to manage games:

| Command | Description |
|---------|-------------|
| `/new <name>` | Create a new game |
| `/load <name>` | Resume a saved game (partial name match works) |
| `/list-games` | Show all saved games |
| `/help` | Show commands |
| `/exit` | Quit |

Regular input (no `/`) is sent to the dungeon master as your action.

---

## Personas and scenarios

Drop `.yml` files into `data/personas/` or `data/scenarios/` to add presets. They appear automatically in the GUI's New Game dialog and are used by `/new` in the CLI.

**Persona format:**
```yaml
persona: "You are a gritty noir detective story narrator..."
```

**Scenario format:**
```yaml
setting: "1920s Chicago. Prohibition is in full swing."
location: "A speakeasy basement on the south side."
```

---

## How it works

After each exchange the LLM updates a compact "game notes" summary (current location, active goals, key NPCs, plot threads). These notes travel in the system prompt even when old messages are dropped, so context is preserved across long sessions.

Games are stored in `~/.storyteller/storyteller.db` (SQLite). A game started in the CLI can be resumed in the GUI and vice versa.

---

## Roadmap

- Character sheet (inventory, skills, stats)
- Manual note editing
- Multiple personas/scenarios in the preset library
- Discord bot interface
- Export session as narrative text
