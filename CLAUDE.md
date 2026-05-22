# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

This project uses `uv` for dependency management.

```bash
# Install dependencies
uv sync

# Flet desktop app (primary interface)
uv run python main.py --gui

# CLI (persistent — same games DB as the GUI)
uv run python main.py
```

There is no test suite yet.

## CLI slash commands

```
/new <name>      Create a new game (uses default persona & scenario from data/)
/load <name>     Load a saved game by name (partial match)
/list-games      List all saved games
/help            Show commands
/exit            Quit
```

During a game, regular input is sent to the LLM. Slash commands still work mid-game.

## YAML presets

`data/personas/*.yml` and `data/scenarios/*.yml` are the preset library. Each file is picked up automatically by both interfaces:

- **CLI**: `/new` loads `default.yml` from each directory.
- **GUI**: New Game dialog shows a dropdown for each directory; selecting a preset fills the text fields.

Adding a new `.yml` file to either directory makes it appear in both interfaces without any code changes.

**Persona format** (`data/personas/*.yml`):
```yaml
persona: "Your persona text here."
```

**Scenario format** (`data/scenarios/*.yml`):
```yaml
setting: "World description."
location: "Starting location."
```

## Architecture

StoryTeller is a single-player narrative RPG where an LLM simulates a dungeon master. Both CLI and GUI share the same SQLite database — games are interchangeable between interfaces.

### Data flow per exchange

```
user sends → LLM streams narrative → messages saved to SQLite
          → second LLM call updates game notes → notes saved to SQLite
```

Game notes always travel in the system prompt regardless of history trimming. This is how long-session context is managed.

### Module map

| File | Purpose |
|------|---------|
| `core/storyteller.py` | OpenAI client. System prompt includes persona + setting + location + notes. `get_notes_update()` runs the second per-exchange call. `HISTORY_LIMIT = 20`. |
| `core/db.py` | SQLite persistence (`~/.storyteller/storyteller.db`). `GameRepository` handles all reads/writes. |
| `core/persona.py` | `load_persona(path)` — load one file. `list_personas()` — scan `data/personas/*.yml`. |
| `core/scenario.py` | `load_scenario(path)` — load one file. `list_scenarios()` — scan `data/scenarios/*.yml`. |
| `ui/cli.py` | Persistent CLI with slash commands and streaming. Uses same DB as GUI. |
| `ui/gui.py` | Flet app entry point. `MessageEntry` widget (edit/save/delete). Routes between screens. |
| `ui/game_select_screen.py` | Game list + New Game dialog with persona/scenario dropdowns. |
| `ui/game_screen.py` | Two-panel chat + notes screen. Streaming in background threads. |

### SQLite schema (3 tables)

- `games` — name, persona, setting, location, timestamps
- `messages` — game_id, role (`user`/`assistant`), content, created_at
- `game_notes` — game_id (unique), notes text, updated_at

### Flet threading model

All LLM calls run in `threading.Thread(daemon=True)`. Never use `asyncio`. `page.update()` is safe to call from any thread in flet 0.28.

## Environment

Copy `.env.template` to `.env`. Required vars:
- `OPENAI_API_KEY` — API key (use `sk-nothing` for local servers)
- `OPENAI_BASE_URL` — endpoint; set to a local Ollama or llama.cpp URL for offline use
- `OPENAI_API_MODEL` — model name, e.g. `gpt-4o-mini` or `gemma4:e4b`

## Dead code (do not use)

- `core/database.py` — old PostgreSQL/SQLAlchemy layer; never imported
- `database/` directory — PostgreSQL schema and scripts; not used
- `config.yml` — old config format; superseded by `.env`
