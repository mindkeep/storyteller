"""SQLite persistence layer for StoryTeller."""

import sqlite3
from pathlib import Path

DB_PATH = Path.home() / ".storyteller" / "storyteller.db"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS games (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    persona     TEXT NOT NULL DEFAULT '',
    setting     TEXT NOT NULL DEFAULT '',
    location    TEXT NOT NULL DEFAULT '',
    created_at  REAL NOT NULL DEFAULT (unixepoch('now')),
    last_played REAL NOT NULL DEFAULT (unixepoch('now'))
);

CREATE TABLE IF NOT EXISTS messages (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id    INTEGER NOT NULL REFERENCES games(id) ON DELETE CASCADE,
    role       TEXT NOT NULL CHECK(role IN ('user','assistant')),
    content    TEXT NOT NULL,
    created_at REAL NOT NULL DEFAULT (unixepoch('now'))
);

CREATE TABLE IF NOT EXISTS game_notes (
    game_id    INTEGER NOT NULL UNIQUE REFERENCES games(id) ON DELETE CASCADE,
    notes      TEXT NOT NULL DEFAULT '',
    updated_at REAL NOT NULL DEFAULT (unixepoch('now'))
);
"""


def init_db(path: Path = DB_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.executescript(_SCHEMA)


class GameRepository:
    def __init__(self, path: Path = DB_PATH):
        self._path = path

    def _connect(self):
        conn = sqlite3.connect(self._path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def create_game(self, name: str, persona: str, setting: str, location: str) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO games (name, persona, setting, location) VALUES (?, ?, ?, ?)",
                (name, persona, setting, location),
            )
            return cur.lastrowid

    def list_games(self) -> list[dict]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM games ORDER BY last_played DESC"
            ).fetchall()
            return [dict(r) for r in rows]

    def get_game(self, game_id: int) -> dict:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM games WHERE id = ?", (game_id,)
            ).fetchone()
            return dict(row) if row else {}

    def update_last_played(self, game_id: int) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE games SET last_played = unixepoch('now') WHERE id = ?",
                (game_id,),
            )

    def add_message(self, game_id: int, role: str, content: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO messages (game_id, role, content) VALUES (?, ?, ?)",
                (game_id, role, content),
            )

    def get_messages(self, game_id: int) -> list[dict]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT role, content FROM messages WHERE game_id = ? ORDER BY created_at ASC",
                (game_id,),
            ).fetchall()
            return [dict(r) for r in rows]

    def get_notes(self, game_id: int) -> str:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT notes FROM game_notes WHERE game_id = ?", (game_id,)
            ).fetchone()
            return row["notes"] if row else ""

    def upsert_notes(self, game_id: int, notes: str) -> None:
        with self._connect() as conn:
            conn.execute(
                """INSERT INTO game_notes (game_id, notes, updated_at)
                   VALUES (?, ?, unixepoch('now'))
                   ON CONFLICT(game_id) DO UPDATE SET notes = excluded.notes,
                   updated_at = excluded.updated_at""",
                (game_id, notes),
            )
