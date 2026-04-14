#!/usr/bin/env python3

import json
import sys
from datetime import datetime, timezone
from xml.sax.saxutils import escape


LATEST_PROMPT_INSTRUCTION = (
    "Use the prompt with the newest timestamp if multiple prompt blocks appear."
)


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def build_wrapped_prompt(
    prompt: str,
    *,
    submitted_at_utc: str | None = None,
) -> str:
    safe_prompt = escape(prompt)
    submitted_at_utc = submitted_at_utc or utc_timestamp()
    safe_instruction = escape(LATEST_PROMPT_INSTRUCTION)

    return (
        f"<instruction>{safe_instruction}</instruction>\n"
        f'<prompt timestamp="{submitted_at_utc}">{safe_prompt}</prompt>\n'
    )


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

    sys.stdout.write(build_wrapped_prompt(prompt))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
