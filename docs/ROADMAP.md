# docs/ROADMAP.md
## Milestone 1: State & Utilities (The Foundation)
* **Goal:** Establish local file operations without network dependencies.
* **Tasks:**
  * Implement `utils.py` (hashing, prompting).
  * Implement `state.py` (atomic read/write of `registry.json`).
  * Add unit tests for hash stability and atomic writes to ensure data integrity.

## Milestone 2: Network Layer
* **Goal:** Safely fetch raw text via HTTP.
* **Tasks:**
  * Implement `network.py`.
  * Add GitHub URL transformation logic.
  * Handle HTTP errors gracefully without exposing stack traces to the user.

## Milestone 3: Core Logic
* **Goal:** Wire state and network modules together.
* **Tasks:**
  * Implement `core.py` functions (`execute_install`, `execute_remove`).
  * Implement the hash comparison logic for safe removal.

## Milestone 4: CLI Interface
* **Goal:** Expose functionality via terminal commands.
* **Tasks:**
  * Implement `cli.py` using `argparse`.
  * Map `install`, `remove`, `list`, and `check` commands to `core.py` functions.
  * Add top-level error catching to return clean exit codes (0-4).
