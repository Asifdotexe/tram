# docs/PRD.md
**Title:** Terminal Router for Agent Modules (TRAM)
**Author:** Asif Sayyed
**Version:** 1.0.0

## 1. Product Vision
A zero-dependency, ultra-lightweight Python CLI that routes AI agent skills from remote repositories to local file systems. It acts purely as a transport and state-tracking layer, enforcing strict modularity and zero bloat.

## 2. In Scope vs. Out of Scope
**In Scope:**
* Fetching raw text/markdown files via HTTP GET.
* Parsing simple JSON manifests (`tram.json`).
* Maintaining local state via `~/.tram/registry.json`.
* SHA-256 hashing for modification detection.
* Interactive prompts for destructive actions.

**Out of Scope:**
* Compiling, parsing, or modifying the content of downloaded skills.
* Resolving complex dependency trees.
* Backward compatibility for legacy IDE or agent formats (TRAM maintains strict boundaries to prioritize user-facing execution speed over development bloat).
* Authentication for private repositories.

## 3. User Stories & Acceptance Criteria
* **US1: Install via Raw URL**
  * *Context:* A user has a raw GitHub URL to a markdown file.
  * *Action:* Runs `tram install <url>`.
  * *Acceptance:* The file is downloaded, placed in the current directory, and recorded in `~/.tram/registry.json` with its SHA-256 hash.
* **US2: Target Mismatch Warning**
  * *Context:* A user installs a skill built for Agent X while using Agent Y.
  * *Action:* Runs `tram install <url> --agent cursor`.
  * *Acceptance:* The CLI detects the mismatch from the manifest, pauses execution, and prompts: `Agent mismatch detected. Proceed? (y/N)`.
* **US3: Safe Removal**
  * *Context:* A user wants to remove a skill they manually edited.
  * *Action:* Runs `tram remove <skill_name>`.
  * *Acceptance:* TRAM hashes the local file, compares it to the registry, detects the change, and prompts for confirmation before deletion.
