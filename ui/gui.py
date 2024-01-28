import customtkinter as ctk
import tkinter as tk

from langchain.memory import ConversationBufferMemory
from langchain.schema.messages import ChatMessage

from ui.baseui import BaseUI
from core import config
from core.llamacpp_utils import init_llamacpp, init_chain

from core.storyteller import StoryTeller, DEFAULT_SETTING

from asyncio import Event,create_task

class GUI(BaseUI):
    """
    GUI interface class
    """

    root: ctk.CTk
    chat_area: tk.Listbox
    user_input: tk.Entry
    delete_button: tk.Button
    edit_button: tk.Button

    def __init__(self, conf: config.Config):
        super().__init__(conf=conf)
        self.root = ctk.CTk()
        self.chat_area = tk.Listbox(self.root)
        self.chat_area.pack()
        self.user_input = tk.Entry(self.root)
        self.user_input.pack()
        self.send_button = tk.Button(self.root, text="Send", command=self.send_input)
        self.send_button.pack(side=tk.RIGHT)

        self.send_event = Event()

    def send_input(self):
        self.send_event.set()

    async def get_input(self) -> str:
        await self.send_event.wait()
        input = self.user_input.get()
        self.chat_area.insert(tk.END, "\n\nYou: " + input)
        self.user_input.delete(0, tk.END)
        return input

    def output(self, text: str) -> None:
        self.chat_area.insert(tk.END, text)

    def get_callback_manager(self) -> None:
        return None

    def run(self) -> None:
        memory = ConversationBufferMemory(memory_key="memory")
        memory.chat_memory.add_message(ChatMessage(role="Setting", content=DEFAULT_SETTING))

        # initialize the LLM
        if self.conf.llm_provider == config.LLMProvider.LLAMACPP:
            llm = init_llamacpp(self.conf.models[0], self)
        else:
            raise NotImplementedError(
                f"LLM provider {self.conf.llm_provider} not implemented."
            )

        storyteller = StoryTeller(
            ui=self,
            llm_chain=init_chain(llm=llm, interface=self, memory=memory),
            memory=memory,
        )
#        create_task(storyteller.run())
        self.root.mainloop()