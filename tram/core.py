import os
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from .network import fetch_payload, transform_github_url
from .state import load_registry, save_registry
from .utils import calculate_sha256, prompt_yes_no

def execute_install(url: str, target_agent: str = None, global_install: bool = False) -> int:
    """Orchestrates network fetch, compatibility checks, disk writes, and state updates."""
    url = transform_github_url(url)
    
    # Try fetching manifest
    manifest_url = url.rsplit("/", 1)[0] + "/tram.json" if "/" in url else ""
    manifest = {}
    if manifest_url:
        manifest_payload, status = fetch_payload(manifest_url)
        if status == 200:
            try:
                manifest = json.loads(manifest_payload.decode('utf-8'))
            except json.JSONDecodeError:
                sys.stderr.write("Error: Invalid Manifest Format\n")
                return 4
                
    # Agent mismatch check
    manifest_agent = manifest.get("target_agent")
    if manifest_agent and target_agent and manifest_agent != target_agent:
        sys.stdout.write(f"Agent mismatch detected (manifest requires '{manifest_agent}').\n")
        if not prompt_yes_no("Proceed?", default=False):
            return 3
            
    # Fetch markdown file
    payload, status = fetch_payload(url)
    if status != 200:
        sys.stderr.write(f"Error: Network or HTTP Error (Status {status})\n")
        return 1
        
    filename = url.split("/")[-1] if "/" in url else "skill.md"
    # The spec for global_install isn't fully detailed, I'll assume standard directory structure or just current dir.
    # "placed in the current directory" according to US1
    install_path = Path.cwd() / filename
    if global_install:
        sys.stdout.write("Global install not fully specified, installing in current directory.\n")
        
    try:
        install_path.write_bytes(payload)
    except OSError:
        sys.stderr.write("Error: File System Permission Error\n")
        return 2
        
    # Calculate hash and update state
    file_hash = calculate_sha256(str(install_path))
    skill_name = manifest.get("name", filename.rsplit(".", 1)[0]) # fallback to filename without ext
    
    state = load_registry()
    state[skill_name] = {
        "source_url": url,
        "install_path": str(install_path.absolute()),
        "target_agent": target_agent or manifest_agent or "",
        "sha256_hash": file_hash,
        "installed_at": datetime.now(timezone.utc).isoformat()
    }
    save_registry(state)
    
    sys.stdout.write(f"Successfully installed '{skill_name}' to {install_path}\n")
    return 0

def execute_remove(skill_name: str) -> int:
    """Looks up path in state, calculates current hash, compares against state hash, prompts if different, deletes file, and removes state entry."""
    state = load_registry()
    if skill_name not in state:
        sys.stderr.write(f"Error: Skill '{skill_name}' not found in registry.\n")
        return 0 # Or another code, but let's just exit
        
    entry = state[skill_name]
    install_path = Path(entry["install_path"])
    
    if install_path.exists():
        current_hash = calculate_sha256(str(install_path))
        if current_hash != entry["sha256_hash"]:
            sys.stdout.write(f"Warning: File {install_path} has been modified since installation.\n")
            if not prompt_yes_no("Are you sure you want to remove it?", default=False):
                return 3
                
        try:
            install_path.unlink()
            sys.stdout.write(f"Deleted {install_path}\n")
        except OSError:
            sys.stderr.write("Error: File System Permission Error\n")
            return 2
    else:
        sys.stdout.write(f"File {install_path} not found on disk, removing from registry.\n")
        
    del state[skill_name]
    save_registry(state)
    sys.stdout.write(f"Successfully removed '{skill_name}' from registry.\n")
    return 0

def execute_list() -> int:
    """Lists all installed skills."""
    state = load_registry()
    if not state:
        sys.stdout.write("No skills installed.\n")
        return 0
        
    for name, entry in state.items():
        sys.stdout.write(f"- {name} ({entry['install_path']})\n")
    return 0

def execute_check() -> int:
    """Checks all installed skills for modifications."""
    state = load_registry()
    if not state:
        sys.stdout.write("No skills installed.\n")
        return 0
        
    modified_count = 0
    for name, entry in state.items():
        install_path = Path(entry["install_path"])
        if not install_path.exists():
            sys.stdout.write(f"[{name}] Missing file: {install_path}\n")
            modified_count += 1
            continue
            
        current_hash = calculate_sha256(str(install_path))
        if current_hash != entry["sha256_hash"]:
            sys.stdout.write(f"[{name}] Modified: {install_path}\n")
            modified_count += 1
        else:
            sys.stdout.write(f"[{name}] OK\n")
            
    if modified_count > 0:
        return 2 # Maybe standard exit code for modifications
    return 0
