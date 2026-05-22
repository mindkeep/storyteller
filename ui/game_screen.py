"""Main game screen: two-panel chat + notes layout with streaming LLM responses."""

import threading
import flet as ft

from core.db import GameRepository
from core.storyteller import StoryTeller, HISTORY_LIMIT
from ui.gui import MessageEntry


class GameScreen(ft.Column):
    def __init__(
        self,
        page: ft.Page,
        game_id: int,
        repo: GameRepository,
        storyteller: StoryTeller,
    ) -> None:
        self._page = page
        self._game_id = game_id
        self._repo = repo
        self._storyteller = storyteller
        self._messages: list[dict] = []
        self._notes: str = ""

        self._chat_controls = ft.ListView(
            expand=2, auto_scroll=True, spacing=4, padding=10
        )
        self._notes_text = ft.Text(
            "No notes yet — start playing!",
            selectable=True,
            size=13,
        )
        self._input_field = ft.TextField(
            hint_text="What do you do?",
            expand=True,
            on_submit=self._on_send,
            shift_enter=True,
        )
        self._send_button = ft.ElevatedButton(
            "Send",
            icon=ft.Icons.SEND,
            on_click=self._on_send,
        )

        self._load_history()
        game = repo.get_game(game_id)
        self._appbar = ft.AppBar(
            title=ft.Text(game.get("name", "StoryTeller")),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        )

        notes_panel = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Game Notes", weight=ft.FontWeight.BOLD, size=14),
                    ft.Divider(height=1),
                    ft.Container(
                        ft.Column([self._notes_text], scroll=ft.ScrollMode.AUTO),
                        expand=True,
                    ),
                ],
            ),
            expand=1,
            padding=10,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            border_radius=8,
            margin=ft.margin.only(top=4, right=8, bottom=4),
        )

        super().__init__(
            controls=[
                ft.Row(
                    [self._chat_controls, notes_panel],
                    expand=True,
                    vertical_alignment=ft.CrossAxisAlignment.STRETCH,
                ),
                ft.Container(
                    ft.Row(
                        [self._input_field, self._send_button],
                        vertical_alignment=ft.CrossAxisAlignment.END,
                    ),
                    padding=ft.padding.symmetric(horizontal=10, vertical=8),
                ),
            ],
            expand=True,
        )

    def _make_entry(self, author: str, message: str) -> MessageEntry:
        def delete_cb(entry: MessageEntry) -> None:
            self._chat_controls.controls.remove(entry)
            self._chat_controls.update()

        return MessageEntry(author, message, on_delete=delete_cb)

    def _load_history(self) -> None:
        messages = self._repo.get_messages(self._game_id)
        self._messages = list(messages)
        for msg in messages:
            author = "You" if msg["role"] == "user" else "AI"
            self._chat_controls.controls.append(self._make_entry(author, msg["content"]))

        self._notes = self._repo.get_notes(self._game_id)
        if self._notes:
            self._notes_text.value = self._notes

    def _on_send(self, e) -> None:
        user_input = self._input_field.value.strip()
        if not user_input:
            return

        self._input_field.value = ""
        self._send_button.disabled = True

        self._chat_controls.controls.append(self._make_entry("You", user_input))
        ai_entry = self._make_entry("AI", "...")
        self._chat_controls.controls.append(ai_entry)
        self._page.update()

        threading.Thread(
            target=self._stream_response,
            args=(user_input, ai_entry),
            daemon=True,
        ).start()

    def _stream_response(self, user_input: str, ai_entry: MessageEntry) -> None:
        try:
            history = self._messages[-HISTORY_LIMIT:]
            response_text = ""

            ai_entry.text_box.value = ""
            self._page.update()

            for chunk in self._storyteller.get_stream_response(
                history, user_input, self._notes
            ):
                response_text += chunk
                ai_entry.text_box.value = response_text
                self._page.update()

            ai_entry.saved_content = response_text

            self._repo.add_message(self._game_id, "user", user_input)
            self._repo.add_message(self._game_id, "assistant", response_text)
            self._messages.append({"role": "user", "content": user_input})
            self._messages.append({"role": "assistant", "content": response_text})

            self._send_button.disabled = False
            self._page.update()

            threading.Thread(
                target=self._update_notes,
                args=(user_input, response_text),
                daemon=True,
            ).start()

        except Exception as exc:
            ai_entry.text_box.value = f"[Error: {exc}]"
            ai_entry.saved_content = ai_entry.text_box.value
            self._send_button.disabled = False
            self._page.update()

    def _update_notes(self, user_input: str, assistant_response: str) -> None:
        try:
            new_notes = self._storyteller.get_notes_update(
                self._notes, user_input, assistant_response
            )
            self._notes = new_notes
            self._repo.upsert_notes(self._game_id, new_notes)
            self._notes_text.value = new_notes
            self._page.update()
        except Exception:
            pass
