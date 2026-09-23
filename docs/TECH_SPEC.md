# docs/TECH_SPEC.md
## 1. System Architecture & Boundaries
* **Language:** Python 3.8+
* **Dependencies:** Strictly standard library (`argparse`, `json`, `urllib.request`, `hashlib`, `os`, `sys`, `pathlib`).
* **Exit Codes:**
  * `0`: Success
  * `1`: Network or HTTP Error
  * `2`: File System Permission Error
  * `3`: User Aborted Action
  * `4`: Invalid URL or Manifest Format

## 2. Directory & Module Layout
* `tram/cli.py`: argparse configuration and command routing.
* `tram/core.py`: Main business logic (install, remove, check).
* `tram/network.py`: urllib HTTP requests and URL transformation.
* `tram/state.py`: JSON registry read/write operations.
* `tram/utils.py`: SHA-256 hashing and user prompts.

## 3. Data Schemas
### 3.1 Registry Schema (`~/.tram/registry.json`)
```json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "type": "object",
  "patternProperties": {
    "^[a-zA-Z0-9_-]+$": {
      "type": "object",
      "properties": {
        "source_url": { "type": "string" },
        "install_path": { "type": "string" },
        "target_agent": { "type": "string" },
        "sha256_hash": { "type": "string" },
        "installed_at": { "type": "string", "format": "date-time" }
      },
      "required": ["source_url", "install_path", "sha256_hash"]
    }
  }
}
```

## 4. Core Function Signatures

- network.py
`def transform_github_url(url: str) -> str`: Converts standard GitHub blob URLs to raw user content URLs.

`def fetch_payload(url: str) -> tuple[bytes, int]`: Executes GET request with a custom User-Agent header (e.g., TRAM-CLI/1.0). Returns payload and HTTP status code.

- utils.py
`def calculate_sha256(filepath: str) -> str:` Reads file in binary chunks to prevent memory bloat.

`def prompt_yes_no(message: str, default: bool = False) -> bool:` Standard terminal prompt waiting for boolean input.

- state.py
`def load_registry() -> dict: Reads ~/.tram/registry.json`. Creates parent directories and returns {} if missing.

`def save_registry(state: dict) -> None`: Atomic write to prevent file corruption.

- core.py
`def execute_install(url: str, target_agent: str = None, global_install: bool = False) -> int`: Orchestrates network fetch, compatibility checks, disk writes, and state updates.

`def execute_remove(skill_name: str) -> int`: Looks up path in state, calculates current hash, compares against state hash, prompts if different, deletes file, and removes state entry.
