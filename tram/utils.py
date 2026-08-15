import hashlib
import sys
from pathlib import Path


def calculate_sha256(filepath: str) -> str:
    """Reads file and calculates SHA-256 hash."""
    try:
        # read_bytes() safely handles context management internally, resulting in cleaner code
        return hashlib.sha256(Path(filepath).read_bytes()).hexdigest()
    except FileNotFoundError:
        return ""


def prompt_yes_no(message: str, default: bool = False) -> bool:
    """Standard terminal prompt waiting for boolean input."""
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default:
        prompt_str = " [Y/n] "
    else:
        prompt_str = " [y/N] "

    while True:
        sys.stdout.write(message + prompt_str)
        choice = input().lower().strip()
        if default is not None and choice == "":
            return default
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")
