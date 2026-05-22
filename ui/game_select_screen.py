"""Game selection and new-game creation screen."""

from datetime import datetime
import flet as ft

from core.db import GameRepository
from core.persona import load_persona, list_personas
from core.scenario import load_scenario, list_scenarios


class GameSelectScreen(ft.Column):
    def __init__(self, page: ft.Page, repo: GameRepository, on_game_selected) -> None:
        self._page = page
        self._repo = repo
        self._on_game_selected = on_game_selected
        self._game_list = ft.ListView(expand=True, spacing=4)

        self._refresh_list()

        super().__init__(
            controls=[
                ft.Container(
                    ft.Text("StoryTeller", size=32, weight=ft.FontWeight.BOLD),
                    margin=ft.margin.only(bottom=4),
                ),
                ft.Text(
                    "Choose a saved game or start a new one.",
                    size=14,
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
                ft.Divider(),
                ft.Container(self._game_list, expand=True),
                ft.ElevatedButton(
                    "New Game",
                    icon=ft.Icons.ADD,
                    on_click=self._open_new_game_dialog,
                ),
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )

    def _refresh_list(self) -> None:
        self._game_list.controls.clear()
        games = self._repo.list_games()
        if not games:
            self._game_list.controls.append(
                ft.Text(
                    "No saved games yet.",
                    color=ft.Colors.ON_SURFACE_VARIANT,
                    italic=True,
                )
            )
        else:
            for game in games:
                last = datetime.fromtimestamp(game["last_played"]).strftime("%b %d, %Y %H:%M")
                game_id = game["id"]
                self._game_list.controls.append(
                    ft.ListTile(
                        title=ft.Text(game["name"], weight=ft.FontWeight.W_500),
                        subtitle=ft.Text(f"Last played: {last}", size=12),
                        trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
                        on_click=lambda e, gid=game_id: self._on_game_selected(gid),
                    )
                )

    def _open_new_game_dialog(self, e) -> None:
        personas = list_personas()
        scenarios = list_scenarios()

        # Seed fields from defaults
        default_persona = load_persona()
        default_scenario = load_scenario()

        name_field = ft.TextField(label="Game name", autofocus=True)
        persona_field = ft.TextField(
            label="Dungeon master persona",
            value=default_persona,
            multiline=True,
            min_lines=3,
            max_lines=5,
        )
        setting_field = ft.TextField(
            label="World setting",
            value=default_scenario.setting,
            multiline=True,
            min_lines=2,
            max_lines=4,
        )
        location_field = ft.TextField(
            label="Starting location",
            value=default_scenario.location,
        )
        error_text = ft.Text("", color=ft.Colors.ERROR, size=12)

        form_controls = [name_field]

        if personas:
            persona_opts = [ft.dropdown.Option(key=str(i), text=p["name"]) for i, p in enumerate(personas)]

            def on_persona_change(ev) -> None:
                idx = int(ev.control.value)
                persona_field.value = personas[idx]["content"]
                self._page.update()

            form_controls.append(
                ft.Dropdown(
                    label="Persona preset",
                    options=persona_opts,
                    value="0",
                    on_change=on_persona_change,
                )
            )

        form_controls.append(persona_field)

        if scenarios:
            scenario_opts = [ft.dropdown.Option(key=str(i), text=s["name"]) for i, s in enumerate(scenarios)]

            def on_scenario_change(ev) -> None:
                idx = int(ev.control.value)
                setting_field.value = scenarios[idx]["setting"]
                location_field.value = scenarios[idx]["location"]
                self._page.update()

            form_controls.append(
                ft.Dropdown(
                    label="Scenario preset",
                    options=scenario_opts,
                    value="0",
                    on_change=on_scenario_change,
                )
            )

        form_controls += [setting_field, location_field, error_text]

        def on_create(ev) -> None:
            if not name_field.value.strip():
                error_text.value = "Game name is required."
                self._page.update()
                return
            game_id = self._repo.create_game(
                name=name_field.value.strip(),
                persona=persona_field.value.strip() or default_persona,
                setting=setting_field.value.strip() or default_scenario.setting,
                location=location_field.value.strip() or default_scenario.location,
            )
            dialog.open = False
            self._page.update()
            self._on_game_selected(game_id)

        def on_cancel(ev) -> None:
            dialog.open = False
            self._page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("New Game"),
            content=ft.Column(
                form_controls,
                tight=True,
                spacing=12,
                width=500,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=on_cancel),
                ft.ElevatedButton("Create", on_click=on_create),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._page.overlay.append(dialog)
        dialog.open = True
        self._page.update()
