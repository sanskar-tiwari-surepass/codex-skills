#!/opt/homebrew/bin/python3

import os
import sys


TARGET = "/Users/sanskartiwari/.codex/hooks/stop_checker_hook.py"


def main() -> int:
    if not os.path.exists(TARGET):
        return 0
    os.execv("/opt/homebrew/bin/python3", ["/opt/homebrew/bin/python3", TARGET, *sys.argv[1:]])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
