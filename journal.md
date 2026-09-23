## DATE: 2026-08-14 23:09
### Goal: Record the SDD decisions we made while designing the Knowledge-Note skill and TRAM.

These are the architectural choices we made, from the first idea to the final spec.

**1. Streamlining the PKM Note Template**
The original 6-section prompt forced users to fill out tables and draw ASCII diagrams. We loosened the rules to make it human-first. Data tables are now conditional, flowcharts and FAQs are gone, and "Nuance & Context" gets its own section. We kept the anti-AI vocabulary rules.

**2. Automating the Skill via Antigravity CLI**
No one wants to paste a huge prompt manually. We turned the template into a reusable `knowledge-note.md` skill that uses `$ARGUMENTS`. Now you can trigger it with a `/knowledge-note` slash command.

**3. Publishing the Custom Skill Repository**
We set up a clean repo layout with a `skills/` folder to share these custom skills. The `.gitignore` tracks editor settings like `settings.json` but ignores local runtime logs, `.env` secrets, and OS files like `.DS_Store`.

**4. Identifying the "Skill Bloat" Problem**
When you download skills into random hidden folders like `~/.gemini` or `.agents/`, you lose track of them. They get outdated and eat up context window tokens. We needed a fast package manager to fix this fragmentation.

**5. Designing the TRAM Package Manager**
*   **Router vs. Compiler:** The tool routes files; it doesn't compile them. Translating between agent formats breaks too often. Moving files means the skill author is responsible if something fails.
*   **Handling Incompatible IDEs:** If someone installs a skill for the wrong agent, we warn them and ask if they want to proceed. We don't block the action entirely.
*   **Target Agents:** Users have to pass an `--agent` flag. We don't guess the environment.
*   **Performance:** We stuck entirely to the Python standard library. Avoiding external dependencies keeps the CLI fast.
*   **State Management:** We used a local JSON registry instead of an SQLite database to avoid unnecessary overhead.
*   **Skill Sourcing:** The tool pulls skills directly from raw Git URLs. A hosted registry costs money and takes time to maintain.
*   **Updates:** The tool checks remote file hashes, but the user has to run the update command themselves, similar to how `package.json` works.
*   **Trigger Collisions:** If two skills use the same command, we don't try to edit the file to fix it, since that might break the prompt. The user has to rename the file or fix it manually.
*   **Modifying & Deleting:** TRAM checks the local file hash against the registry. If someone edited a file locally, it asks for confirmation before deleting it.
*   **Global State:** Global configs and skills live in `~/.tram/`.
*   **Defining a "Skill":** The tool handles both plain markdown files and repo URLs that include a `tram.json` manifest. This works for quick shares and complex packages.
*   **Naming the Tool:** We named it TRAM (Terminal Router for Agent Modules). It avoids PATH conflicts with tools like `pack` or `yasm` and fits the idea of routing files rather than compiling them.


## Date: 15-08-2026

- Implement prek and precommit ruff checks
- Learnt that we don't need to use isort if we are using ruff, just need to add 
```toml
[tool.ruff.lint]
extend-select = ["I"]
```
into the pyproject.toml file
- We're now hashing the payload variable that is already sitting in memory, entirely skipping the step where we were needlessly re-reading the file from disk right after writing it.
- The file-hashing utility was shrunk using Path(filepath).read_bytes(). I left a comment explaining that this avoids manual context management and chunking loops since the pathlib method cleanly and safely handles the file I/O for us.
