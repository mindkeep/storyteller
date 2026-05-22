import yaml
from pathlib import Path
from pydantic import BaseModel

_DATA_DIR = Path(__file__).parent.parent / "data" / "scenarios"

_FALLBACK_SETTING = "A classic fantasy world of mystery and adventure."
_FALLBACK_LOCATION = "A crossroads at the edge of an ancient forest"


class Scenario(BaseModel):
    setting: str
    location: str


def load_scenario(path: str = None) -> Scenario:
    if path is None:
        path = _DATA_DIR / "default.yml"
    try:
        with open(path, mode="r", encoding="utf-8") as f:
            return Scenario(**yaml.safe_load(f))
    except (FileNotFoundError, KeyError, TypeError):
        return Scenario(setting=_FALLBACK_SETTING, location=_FALLBACK_LOCATION)


def list_scenarios() -> list[dict]:
    """Return all scenario presets found in data/scenarios/. Each entry has 'name', 'path', 'setting', 'location'."""
    results = []
    if not _DATA_DIR.exists():
        return results
    for yml in sorted(_DATA_DIR.glob("*.yml")):
        try:
            data = yaml.safe_load(yml.read_text(encoding="utf-8"))
            results.append({
                "name": yml.stem.replace("_", " ").title(),
                "path": str(yml),
                "setting": data.get("setting", ""),
                "location": data.get("location", ""),
            })
        except Exception:
            pass
    return results
