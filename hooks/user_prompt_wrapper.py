#!/usr/bin/env python3

import json
import sys


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    if payload.get("hook_event_name") != "UserPromptSubmit":
        return 0

    prompt = payload.get("prompt")
    if not isinstance(prompt, str) or not prompt:
        return 0

    sys.stdout.write(f"<prompt>{prompt}</prompt>\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
