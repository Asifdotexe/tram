import argparse
import sys

from .core import execute_check, execute_install, execute_list, execute_remove


def main() -> None:
    """
    Entrypoint for tram
    """
    parser = argparse.ArgumentParser(description="Terminal Router for Agent Modules (TRAM)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # install command
    install_parser = subparsers.add_parser("install", help="Install a skill from a URL")
    _ = install_parser.add_argument("url", help="Raw GitHub URL to a markdown file")
    _ = install_parser.add_argument("--agent", help="Target agent for compatibility check")
    _ = install_parser.add_argument("--global", dest="global_install", action="store_true", help="Install globally")

    # remove command
    remove_parser = subparsers.add_parser("remove", help="Remove an installed skill")
    _ = remove_parser.add_argument("skill_name", help="Name of the skill to remove")

    # list command
    _ = subparsers.add_parser("list", help="List installed skills")

    # check command
    _ = subparsers.add_parser("check", help="Check integrity of installed skills")

    args = parser.parse_args()

    if args.command == "install":
        sys.exit(execute_install(args.url, args.agent, args.global_install))
    elif args.command == "remove":
        sys.exit(execute_remove(args.skill_name))
    elif args.command == "list":
        sys.exit(execute_list())
    elif args.command == "check":
        sys.exit(execute_check())


if __name__ == "__main__":
    main()
