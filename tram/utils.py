import hashlib
import sys

def calculate_sha256(filepath: str) -> str:
    """Reads file and calculates SHA-256 hash."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            sha256_hash.update(f.read())
        return sha256_hash.hexdigest()
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
