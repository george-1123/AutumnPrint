import argparse
import sys
from pathlib import Path

from autumn_control.orders import show_order


def main():
    parser = argparse.ArgumentParser(prog="autumn")
    commands = parser.add_subparsers(dest="command", required=True)
    show = commands.add_parser("show-order")
    show.add_argument("--fixture", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(show_order(args.fixture))
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
