import yaml


def load_persona(path: str = "data/personas/default.yml") -> str:
    """
    Load persona from a yaml file
    """
    with open(file=path, mode="r", encoding="utf-8") as file:
        return yaml.safe_load(file)["persona"]
