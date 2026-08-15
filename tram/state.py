"""
Persistent state management and registry tracking.

This module is responsible for reading and writing the `registry.json` file,
which acts as the database for all installed skills. It uses atomic file
operations to prevent corruption during writes. It is exclusively called by
`core.py` whenever the installation state changes or needs to be queried.
"""

import json
import os
import tempfile
from pathlib import Path

REGISTRY_DIR = Path.home() / ".tram"
REGISTRY_FILE = REGISTRY_DIR / "registry.json"


def load_registry() -> dict[str, dict[str, str]]:
    """
    Reads the state registry from ~/.tram/registry.json.

    :return: A dictionary mapping skill names to their installation metadata.
    """
    if not REGISTRY_FILE.exists():
        return {}

    try:
        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_registry(state: dict[str, dict[str, str]]) -> None:
    """
    Atomically writes the registry state to disk to prevent file corruption.

    :param state: The registry dictionary containing all installed skills metadata.
    :raises OSError: If the temporary file cannot be written or replaced.
    """
    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)

    # Write to a temporary file in the same directory to ensure atomic rename
    fd, temp_path = tempfile.mkstemp(dir=REGISTRY_DIR, prefix="registry_", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        # Atomically replace the target file
        os.replace(temp_path, REGISTRY_FILE)
    except Exception:
        # Clean up temporary file in case of error
        try:
            os.remove(temp_path)
        except OSError:
            pass
        raise
