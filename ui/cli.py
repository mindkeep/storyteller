"""
This module provides the CLI interface
"""

from core.persona import load_persona
from core.scenario import load_scenario
from core.storyteller import StoryTeller

from openai import APIConnectionError

class CLI:
    """
    CLI interface class
    """

    def handle_command(self, command: str) -> None:
        """
        Handle the given command
        """
        command = command.lower()
        if command.startswith("/"):
            command = command[1:]
        if command == "exit":
            print("Goodbye!")
            exit(0)
        else:
            print(f"Unknown command: {command}")

    def run(self) -> None:
        """
        Run the CLI interface
        """

        welcome_str = "Welcome to the StoryTeller CLI!"
        print(welcome_str)
        print("=" * len(welcome_str))

        persona = load_persona()
        scenario = load_scenario()

        print(f"Location: {scenario.location}")
        print(f"Setting: {scenario.setting}")

        storyteller = StoryTeller(
            persona=persona,
            setting=scenario.setting,
            location=scenario.location,
        )

        print("(Type '/exit' to exit the application.)\n")

        msg_history = []
        while True:
            try:
                user_input = input("\nYou: ")
            except KeyboardInterrupt:
                # exit loop and close chat
                break

            if user_input in ["/exit", "/quit"]:
                # exit loop and close chat
                break

            try:
                llm_out = storyteller.get_stream_response(
                    msg_history=msg_history, user_input=user_input
                )

                print("AI: ", end="")
                response = ""
                for chunk in llm_out:
                    print(chunk, end="")
                    response += chunk
            except APIConnectionError as api_err:
                print(f"API Connection Error: {api_err}")
                print("Please check your internet connection and try again.")
                exit(1)

            msg_history.append({"role": "user", "content": user_input})
            msg_history.append({"role": "assistant", "content": response})

        print("\nExiting...")
