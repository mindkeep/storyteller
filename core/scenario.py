from pydantic import BaseModel
import yaml


class Scenario(BaseModel):
    setting: str
    location: str


def load_scenario(path: str = "data/scenarios/default.yml") -> Scenario:
    """
    Create a scenario from a yaml file
    """
    with open(file=path, mode="r", encoding="utf-8") as file:
        return Scenario(**yaml.safe_load(file))
