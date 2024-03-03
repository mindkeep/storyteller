import yaml

class Scenario:
    """
    Class for scenario
    """

    def __init__(self, setting: str, location: str) -> None:
        """
        Initialize the scenario
        """
        self.setting = setting
        self.location = location
    
    @classmethod
    def from_yaml(cls, path: str) -> Scenario:
        """
        Create a scenario from a yaml file
        """
        with open(file=path, mode="r", encoding="utf-8") as file:
            scenario = yaml.safe_load(file)
            return cls(
                setting=scenario["setting"],
                location=scenario["location"]
            )