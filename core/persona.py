import yaml

class Persona:
    """
    Class for persona
    """

    def __init__(self, persona: str) -> None:
        """
        Initialize the persona
        """
        self.persona = persona

    @classmethod
    def from_yaml(cls, path: str) -> Persona:
        """
        Create a persona from a yaml file
        """
        with open(file=path, mode="r", encoding="utf-8") as file:
            persona = yaml.safe_load(file)
            return cls(
                persona=persona["persona"]
            )