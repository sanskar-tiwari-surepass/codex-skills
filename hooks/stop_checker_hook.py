#!/opt/homebrew/bin/python3

import json
import os
import re
import sqlite3
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


SOUND_PATH = Path("/Users/sanskartiwari/.codex/assets/town-bell.mp3")
STATUS_VALUES = {"done", "continue", "blocked"}
MARKER = "$stop-checker"


def resolve_state_db():
    home = Path(os.path.expanduser("~/.codex"))
    configured = os.environ.get("CODEX_SQLITE_HOME")
    if configured:
        candidate = Path(configured).expanduser() / "state_5.sqlite"
        if candidate.exists():
            return candidate
    candidate = home / "state_5.sqlite"
    if candidate.exists():
        return candidate
    return None


def load_payload():
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def is_root_thread(session_id):
    if not session_id:
        return True

    db_path = resolve_state_db()
    if db_path is None:
        return True

    try:
        conn = sqlite3.connect(db_path)
        try:
            row = conn.execute(
                "select agent_role from threads where id = ? limit 1",
                (session_id,),
            ).fetchone()
        finally:
            conn.close()
    except Exception:
        return True

    if row is None:
        return True

    agent_role = row[0]
    return not agent_role


def ring_bell(session_id):
    if not is_root_thread(session_id):
        return
    if not SOUND_PATH.exists():
        return
    afplay = "/usr/bin/afplay"
    if not os.path.exists(afplay):
        return
    try:
        subprocess.Popen(
            [afplay, str(SOUND_PATH)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    except Exception:
        return


def iter_rollout_events(transcript_path):
    if not transcript_path:
        return
    path = Path(transcript_path)
    if not path.exists():
        return
    with path.open(errors="ignore") as handle:
        for line in handle:
            try:
                yield json.loads(line)
            except Exception:
                continue


def marker_active_for_thread(transcript_path):
    for item in iter_rollout_events(transcript_path) or []:
        if item.get("type") != "response_item":
            continue
        payload = item.get("payload", {})
        if payload.get("type") != "message" or payload.get("role") != "user":
            continue
        text = " ".join(
            chunk.get("text", "")
            for chunk in payload.get("content", [])
            if chunk.get("type") == "input_text"
        )
        if MARKER in text:
            return True
    return False


def parse_stop_xml(last_assistant_message):
    if not last_assistant_message:
        return None, "No final assistant message was available for stop-checking."

    matches = list(re.finditer(r"<stop_checker>.*?</stop_checker>", last_assistant_message, re.S | re.I))
    if not matches:
        return None, "No <stop_checker> XML artifact was found in the latest assistant message."

    xml_text = matches[-1].group(0)
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        return None, f"Invalid <stop_checker> XML artifact: {exc}."

    status = (root.findtext("status") or "").strip().lower()
    reason = (root.findtext("reason") or "").strip()
    completion_evidence = (root.findtext("completion_evidence") or "").strip()

    if status not in STATUS_VALUES:
        return None, "The <stop_checker> XML must include a valid <status> of done, continue, or blocked."
    if not reason:
        return None, "The <stop_checker> XML must include a non-empty <reason>."
    if status == "done" and not completion_evidence:
        return None, "The <stop_checker> XML must include non-empty <completion_evidence> when status is done."

    return {
        "status": status,
        "reason": reason,
        "completion_evidence": completion_evidence,
    }, None


def build_continuation_prompt(error_message=None, decision=None):
    if decision is None:
        return "\n".join(
            [
                "$stop-checker is active for this thread.",
                "Your last stop attempt is invalid.",
                "Do not end the turn yet.",
                error_message or "A valid <stop_checker> XML artifact is required before stopping.",
                "Do not reply with XML only. First provide the normal user-facing answer, then append one compact XML block at the very end.",
                "If you are not unquestionably complete, prefer continue.",
                "Most stop-checked turns should use continue, not done.",
                "Append a final XML block like:",
                "<stop_checker><status>continue</status><reason>short reason</reason></stop_checker>",
                "Allowed status values are continue, blocked, and done.",
                "Use done only when the requested work is actually complete, and include <completion_evidence> for done.",
            ]
        )

    if decision["status"] == "done":
        return None

    if decision["status"] == "continue":
        prefix = "$stop-checker says this thread should continue."
    else:
        prefix = "$stop-checker says this thread is blocked and should not end as complete."

    return "\n".join(
        [
            prefix,
            f"Reason: {decision['reason']}",
            "Continue working in this thread.",
            "Do not reply with XML only. Give the normal user-facing answer first, then append an updated <stop_checker> XML artifact at the very end.",
            "If you are uncertain, prefer continue over a false done.",
            "Most stop-checked turns should use continue, not done.",
        ]
    )


def main():
    payload = load_payload()
    if payload.get("hook_event_name") != "Stop":
        return 0

    ring_bell(payload.get("session_id"))

    transcript_path = payload.get("transcript_path")
    if not marker_active_for_thread(transcript_path):
        return 0

    decision, error_message = parse_stop_xml(payload.get("last_assistant_message"))
    prompt = build_continuation_prompt(error_message=error_message, decision=decision)
    if prompt is None:
        return 0

    sys.stderr.write(prompt + "\n")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
