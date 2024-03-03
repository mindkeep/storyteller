"""
Main flet entry point to have a dialogue with the user and an LLM
"""

import core.config

import flet as ft


class MessageEntry(ft.UserControl):
    """
    Message entry control
    """

    def __init__(self, author: str, message: str, parent: ft.Column) -> None:
        """
        Initialize the message entry control
        """
        super().__init__()
        self.author = author
        self.saved_content = message
        # leave a reference to the parent control to be able to remove
        self.me_parent = parent

    def build(self) -> ft.Control:
        """
        Build the message entry control
        """

        self.text_box = ft.TextField(
            label=self.author,
            value=self.saved_content,
            multiline=True,
            disabled=True,
            expand=True,
        )

        def on_edit(_: ft.ControlEvent) -> None:
            self.edit_button.visible = False
            self.save_button.visible = True
            self.cancel_button.visible = True
            self.delete_button.visible = False
            self.text_box.disabled = False
            self.update()

        self.edit_button = ft.ElevatedButton(text="Edit", on_click=on_edit)

        def on_save(_: ft.ControlEvent) -> None:
            self.saved_content = self.text_box.value
            self.edit_button.visible = True
            self.save_button.visible = False
            self.cancel_button.visible = False
            self.delete_button.visible = True
            self.text_box.disabled = True
            self.update()

        self.save_button = ft.ElevatedButton(
            text="Save", on_click=on_save, visible=False
        )

        def on_cancel(_: ft.ControlEvent) -> None:
            self.text_box.value = self.saved_content
            self.edit_button.visible = True
            self.save_button.visible = False
            self.cancel_button.visible = False
            self.delete_button.visible = True
            self.text_box.disabled = True
            self.update()

        self.cancel_button = ft.ElevatedButton(
            text="Cancel", on_click=on_cancel, visible=False
        )

        def on_delete(_: ft.ControlEvent) -> None:
            self.me_parent.controls.remove(self)
            self.me_parent.update()

        self.delete_button = ft.ElevatedButton(text="Delete", on_click=on_delete)

        return ft.Row(
            controls=[
                self.text_box,
                self.edit_button,
                self.save_button,
                self.cancel_button,
                self.delete_button,
            ]
        )


class STMainPage(ft.UserControl):
    """
    Main page for the StoryTeller application
    """

    def __init__(self, conf: core.config.Config) -> None:
        """
        Initialize the main page
        """
        super().__init__()
        self.conf = conf

    def build(self) -> ft.Control:
        """
        Build the main page
        """
        msg_hist = ft.Column()
        msg_hist.controls.append(
            MessageEntry(
                author="Setting",
                message="Welcome to the StoryTeller GUI!",
                parent=msg_hist,
            )
        )
        msg_hist.controls.append(
            MessageEntry(
                author="AI",
                message="Type 'exit' to exit the application.",
                parent=msg_hist,
            )
        )
        input_box = ft.TextField(label="You", expand=True, multiline=True)

        def on_send(_: ft.ControlEvent) -> None:

            msg_hist.controls.append(
                MessageEntry(
                    author="You",
                    message=str(input_box.value),
                    parent=msg_hist,
                )
            )
            input_box.value = ""
            self.update()
            input_box.focus()
        send_button = ft.ElevatedButton(text="Send", on_click=on_send)
        
        col = ft.Column()
        col.controls.append(msg_hist)
        col.controls.append(
            ft.Row(
                controls=[input_box, send_button],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

        return col


def main(page: ft.Page) -> None:
    """
    Main entry point for the StoryTeller GUI
    """
    conf = config.load_config(path="config.yml")
    page.title = "StoryTeller"
    page.theme = ft.Theme(color_scheme_seed="green")
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.ALWAYS
    page.add(STMainPage(conf))

def run(web: bool = False) -> None:
    """
    Run the StoryTeller application
    """

    if web:
        ft.app(target=main, view=ft.AppView.WEB_BROWSER)
    else:
        ft.app(target=main)


if __name__ == "__main__":
    run()
