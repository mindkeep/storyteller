"""
This module contains the base interface class
"""

class UIBaseInterface:
    """
    Interface class
    """

    def __init__(self) -> None:
        """
        Initialize the interface
        """

    def output(self, text: str) -> None:
        """
        Output text to the interface
        """
        raise NotImplementedError("Interface is a base class and cannot be instantiated.")

    def get_input(self) -> str:
        """
        Get input from the interface
        """
        raise NotImplementedError("Interface is a base class and cannot be instantiated.")

    def get_callback_manager(self) -> None:
        """
        Get the callback manager
        """
        raise NotImplementedError("Interface is a base class and cannot be instantiated.")
