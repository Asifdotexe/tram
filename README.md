# TRAM (Terminal Router for Agent Modules)

A zero-dependency file router for AI skills that handles fetching, hashing, and state management locally.

## Usage

Since the project uses `uv` for dependency and environment management, you can run TRAM commands directly from the source directory without formal installation.

### 1. Install a Skill
Download a markdown skill file from GitHub. TRAM will download it, securely hash it, and add it to your internal registry.
```bash
uv run tram install "https://github.com/user/repo/blob/main/skill.md"
```
*Optional flags:*
- `--agent "agent-name"`: Enforce compatibility checking for a specific agent.
- `--global`: Flag the skill for global installation.

### 2. List Installed Skills
See everything you have currently installed along with their absolute file paths on your machine.
```bash
uv run tram list
```

### 3. Check for Tampering
Run an audit on all installed skills. TRAM recalculates the SHA-256 hash of the local files and compares them against the original hashes in the registry, warning you if anything has been modified.
```bash
uv run tram check
```

### 4. Remove a Skill
Cleanly delete the skill file from your disk and remove its entry from the TRAM registry.
```bash
uv run tram remove "skill_name"
```
