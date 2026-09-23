"""
Entry point for the TRAM application.

This module allows the package to be executed directly via `python -m tram`.
It simply delegates execution to the `main()` function defined in `cli.py`.
"""

from .cli import main

if __name__ == "__main__":
    main()
