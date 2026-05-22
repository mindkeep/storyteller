# Design

StoryTeller is a single-player narrative RPG powered by an LLM dungeon master.

## Core idea

The player types free-form actions. The LLM narrates outcomes. There are no hard mechanics — the world is shaped entirely by the narrative.

After every exchange the LLM maintains a compact "game notes" block: current location, active goals, key NPCs, plot threads. This block is always in the system prompt regardless of how much chat history has been trimmed, ensuring the DM never "forgets" important context.

## Unified CLI + GUI

Both interfaces share the same SQLite database. A game started in the CLI can be resumed in the GUI and vice versa.

### CLI slash commands

```
/new <name>      Create a game using default YAML presets
/load <name>     Resume a game (partial name match)
/list-games      List all saved games
/help            Show commands
/exit            Quit
```

Regular input (no leading `/`) is sent to the LLM as a player action.

### GUI

- Game select screen: list of saved games + New Game button
- New Game dialog: persona/scenario dropdowns populated from YAML preset files, with editable text fields
- Game screen: chat panel (left) + notes panel (right), input bar at bottom

## YAML preset system

Files in `data/personas/*.yml` and `data/scenarios/*.yml` are the preset library. Both interfaces discover presets automatically from these directories — no code changes needed to add new settings or personas.

**To add a new scenario:** create `data/scenarios/my_world.yml` with `setting` and `location` keys. It will appear in the GUI dropdown and can be referenced by name.

## Context management

```
flowchart TD
    input[Player action] --> chat[LLM streams narrative]
    chat --> save[Save messages to DB]
    save --> notes[LLM updates game notes ≤200 words]
    notes --> db2[Save notes to DB]
    db2 --> next[Next exchange]
```

- Last `HISTORY_LIMIT = 20` messages sent to LLM per call
- Game notes (always ≤200 words) always included in system prompt
- On resume: full history shown in UI, last 20 sent to LLM, notes restored

## UI layout (GUI)

```
┌─ AppBar (game name) ──────────────────────────────────┐
│                                                        │
│  Chat history (scrollable)    │  Game Notes panel      │
│  ── MessageEntry widgets ──   │  ── updated by LLM ──  │
│  ── edit/save/delete ─────    │                        │
│                                                        │
├─ Input field ────────────────────────── [Send] ────────┤
```

## Future directions

- Character sheet panel (inventory, skills, stats)
- Multiple personas/scenarios in the preset library
- Manual note editing
- Export session as narrative text
- Discord bot interface
