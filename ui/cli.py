"""CLI interface — persistent games with slash commands."""

from datetime import datetime

from dotenv import load_dotenv
from openai import APIConnectionError, AuthenticationError

from core.db import init_db, GameRepository
from core.persona import load_persona, list_personas
from core.scenario import load_scenario, list_scenarios
from core.storyteller import StoryTeller, HISTORY_LIMIT

_HELP = """\
Commands:
  /new <name>        Create a new game (uses default persona & scenario)
  /load <name>       Load a saved game by name (partial match ok)
  /list-games        Show all saved games
  /help              Show this message
  /exit              Quit
"""

_HISTORY_PREVIEW = 6  # message pairs to print when resuming a game


class CLI:
    def __init__(self) -> None:
        load_dotenv()
        init_db()
        self._repo = GameRepository()
        self._game: dict | None = None
        self._storyteller: StoryTeller | None = None
        self._messages: list[dict] = []
        self._notes: str = ""

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    def run(self) -> None:
        print("StoryTeller")
        print("===========")
        print(_HELP)

        while True:
            prompt = "(no game) > " if self._game is None else "You: "
            try:
                user_input = input(prompt).strip()
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                break

            if not user_input:
                continue

            if user_input.startswith("/"):
                if not self._handle_command(user_input):
                    break
            elif self._game is None:
                print("No game loaded. Use /new <name> or /load <name>.")
            else:
                self._chat(user_input)

    # ------------------------------------------------------------------
    # Commands
    # ------------------------------------------------------------------

    def _handle_command(self, raw: str) -> bool:
        """Return False to exit the loop."""
        parts = raw[1:].split(None, 1)
        cmd = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else ""

        if cmd == "exit":
            print("Goodbye!")
            return False
        elif cmd == "help":
            print(_HELP)
        elif cmd == "new":
            self._cmd_new(arg)
        elif cmd == "list-games":
            self._cmd_list_games()
        elif cmd == "load":
            self._cmd_load(arg)
        else:
            print(f"Unknown command: /{cmd}. Type /help for help.")
        return True

    def _cmd_new(self, name: str) -> None:
        if not name:
            print("Usage: /new <game-name>")
            return
        persona = load_persona()
        scenario = load_scenario()
        game_id = self._repo.create_game(
            name=name,
            persona=persona,
            setting=scenario.setting,
            location=scenario.location,
        )
        print(f"\nGame '{name}' created.")
        self._start_game(game_id)

    def _cmd_list_games(self) -> None:
        games = self._repo.list_games()
        if not games:
            print("No saved games.")
            return
        print()
        for g in games:
            marker = " *" if self._game and g["id"] == self._game["id"] else ""
            last = datetime.fromtimestamp(g["last_played"]).strftime("%b %d %Y %H:%M")
            print(f"  {g['name']}{marker}  (last played: {last})")
        print()

    def _cmd_load(self, name: str) -> None:
        if not name:
            print("Usage: /load <game-name>")
            return
        games = self._repo.list_games()
        matches = [g for g in games if name.lower() in g["name"].lower()]
        if not matches:
            print(f"No game found matching '{name}'.")
            return
        if len(matches) > 1:
            print("Multiple matches — be more specific:")
            for g in matches:
                print(f"  {g['name']}")
            return
        self._start_game(matches[0]["id"])

    # ------------------------------------------------------------------
    # Game session
    # ------------------------------------------------------------------

    def _start_game(self, game_id: int) -> None:
        game = self._repo.get_game(game_id)
        self._repo.update_last_played(game_id)
        self._game = game
        self._storyteller = StoryTeller(
            persona=game["persona"],
            setting=game["setting"],
            location=game["location"],
        )
        self._messages = self._repo.get_messages(game_id)
        self._notes = self._repo.get_notes(game_id)

        print(f"\n--- {game['name']} ---")
        print(f"Setting: {game['setting']}")
        if self._notes:
            print(f"\n[Game notes]\n{self._notes}")
        if self._messages:
            print(f"\n[Last {_HISTORY_PREVIEW} messages]")
            for msg in self._messages[-_HISTORY_PREVIEW:]:
                speaker = "You" if msg["role"] == "user" else "AI"
                print(f"{speaker}: {msg['content']}")
        print()

    def _chat(self, user_input: str) -> None:
        try:
            print("AI: ", end="", flush=True)
            response = ""
            for chunk in self._storyteller.get_stream_response(
                self._messages[-HISTORY_LIMIT:], user_input, self._notes
            ):
                print(chunk, end="", flush=True)
                response += chunk
            print()

            self._repo.add_message(self._game["id"], "user", user_input)
            self._repo.add_message(self._game["id"], "assistant", response)
            self._messages.append({"role": "user", "content": user_input})
            self._messages.append({"role": "assistant", "content": response})

            try:
                new_notes = self._storyteller.get_notes_update(
                    self._notes, user_input, response
                )
                self._notes = new_notes
                self._repo.upsert_notes(self._game["id"], new_notes)
            except Exception:
                pass

        except APIConnectionError as exc:
            print(f"\n[Connection error: {exc}]")
        except AuthenticationError as exc:
            print(f"\n[Auth error: {exc}]")
