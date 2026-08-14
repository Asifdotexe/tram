import json
import os
import tempfile
from pathlib import Path

REGISTRY_DIR = Path.home() / ".tram"
REGISTRY_FILE = REGISTRY_DIR / "registry.json"

def load_registry() -> dict:
    """Reads ~/.tram/registry.json. Returns {} if missing."""
    if not REGISTRY_FILE.exists():
        return {}
    
    try:
        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}

def save_registry(state: dict) -> None:
    """Atomic write to prevent file corruption."""
    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
    
    # Write to a temporary file in the same directory to ensure atomic rename
    fd, temp_path = tempfile.mkstemp(dir=REGISTRY_DIR, prefix="registry_", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        # Atomically replace the target file
        os.replace(temp_path, REGISTRY_FILE)
    except Exception as e:
        # Clean up temporary file in case of error
        try:
            os.remove(temp_path)
        except OSError:
            pass
        raise e
