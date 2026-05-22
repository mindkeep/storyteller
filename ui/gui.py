"""Flet app entry point and shared MessageEntry widget."""

import flet as ft


class MessageEntry(ft.Row):
    """Chat message widget with inline edit/save/delete."""

    def __init__(self, author: str, message: str, on_delete=None) -> None:
        self.saved_content = message
        self._on_delete_cb = on_delete

        self.text_box = ft.TextField(
            label=author,
            value=message,
            multiline=True,
            disabled=True,
            expand=True,
        )
        self.edit_button = ft.ElevatedButton(text="Edit", on_click=self._on_edit)
        self.save_button = ft.ElevatedButton(text="Save", on_click=self._on_save, visible=False)
        self.cancel_button = ft.ElevatedButton(text="Cancel", on_click=self._on_cancel, visible=False)
        self.delete_button = ft.ElevatedButton(text="Delete", on_click=self._on_delete)

        super().__init__(
            controls=[
                self.text_box,
                self.edit_button,
                self.save_button,
                self.cancel_button,
                self.delete_button,
            ]
        )

    def _on_edit(self, e) -> None:
        self.edit_button.visible = False
        self.save_button.visible = True
        self.cancel_button.visible = True
        self.delete_button.visible = False
        self.text_box.disabled = False
        self.text_box.focus()
        self.update()

    def _on_save(self, e) -> None:
        self.saved_content = self.text_box.value
        self.edit_button.visible = True
        self.save_button.visible = False
        self.cancel_button.visible = False
        self.delete_button.visible = True
        self.text_box.disabled = True
        self.update()

    def _on_cancel(self, e) -> None:
        self.text_box.value = self.saved_content
        self.edit_button.visible = True
        self.save_button.visible = False
        self.cancel_button.visible = False
        self.delete_button.visible = True
        self.text_box.disabled = True
        self.update()

    def _on_delete(self, e) -> None:
        if self._on_delete_cb:
            self._on_delete_cb(self)


def main(page: ft.Page) -> None:
    from dotenv import load_dotenv
    from core.db import init_db, GameRepository
    from core.storyteller import StoryTeller
    from ui.game_select_screen import GameSelectScreen
    from ui.game_screen import GameScreen

    load_dotenv()
    init_db()
    repo = GameRepository()

    page.title = "StoryTeller"
    page.theme = ft.Theme(color_scheme_seed="green")
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 1100
    page.window.min_width = 700

    def on_game_selected(game_id: int) -> None:
        game = repo.get_game(game_id)
        repo.update_last_played(game_id)
        storyteller = StoryTeller(
            persona=game["persona"],
            setting=game["setting"],
            location=game["location"],
        )
        screen = GameScreen(page, game_id, repo, storyteller)
        page.appbar = screen._appbar
        page.controls.clear()
        page.add(screen)

    page.add(GameSelectScreen(page, repo, on_game_selected))


def run(web: bool = False) -> None:
    if web:
        ft.app(target=main, view=ft.AppView.WEB_BROWSER)
    else:
        ft.app(target=main)


if __name__ == "__main__":
    run()
