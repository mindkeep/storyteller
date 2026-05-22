import yaml
from pathlib import Path

_DATA_DIR = Path(__file__).parent.parent / "data" / "personas"

_FALLBACK = (
    "You are a creative and atmospheric dungeon master. You paint vivid scenes, "
    "give NPCs distinct voices, and let the player's choices shape the story. "
    "You are fair but consequential — actions have real effects on the world. "
    "Keep responses concise (2-4 sentences) unless the moment calls for more."
)


def load_persona(path: str = None) -> str:
    if path is None:
        path = _DATA_DIR / "default.yml"
    try:
        with open(path, mode="r", encoding="utf-8") as f:
            return yaml.safe_load(f)["persona"]
    except (FileNotFoundError, KeyError):
        return _FALLBACK


def list_personas() -> list[dict]:
    """Return all persona presets found in data/personas/. Each entry has 'name', 'path', 'content'."""
    results = []
    if not _DATA_DIR.exists():
        return results
    for yml in sorted(_DATA_DIR.glob("*.yml")):
        try:
            content = yaml.safe_load(yml.read_text(encoding="utf-8")).get("persona", "")
            results.append({"name": yml.stem.replace("_", " ").title(), "path": str(yml), "content": content})
        except Exception:
            pass
    return results
