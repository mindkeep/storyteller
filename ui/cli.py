"""
This module provides the CLI interface
"""

from core.persona import load_persona
from core.scenario import load_scenario
from core.storyteller import StoryTeller


class CLI:
    """
    CLI interface class
    """

    def run(self) -> None:
        """
        Run the CLI interface
        """

        welcome_str = "Welcome to the StoryTeller CLI!"
        # print the welcome message
        print(welcome_str)
        print("=" * len(welcome_str))

        persona = load_persona()
        scenario = load_scenario()

        storyteller = StoryTeller(
            persona=persona,
            setting=scenario.setting,
            location=scenario.location,
        )

        print("Type 'exit' to exit the application.\n")

        msg_history = []
        while True:
            user_input = input("\n\nYou: ")
            if user_input in ["exit", "quit"]:
                break
            else:
                llm_out = storyteller.get_stream_response(
                    msg_history=msg_history, user_input=user_input
                )
                print("AI: ", end="")
                response = ""
                for chunk in llm_out:
                    print(chunk, end="")
                    response += chunk
                msg_history.append({"role": "user", "content": user_input})
                msg_history.append({"role": "assistant", "content": response})
