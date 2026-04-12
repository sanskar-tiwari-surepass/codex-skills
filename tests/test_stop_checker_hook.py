import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "hooks" / "stop_checker_hook.py"
SPEC = importlib.util.spec_from_file_location("stop_checker_hook", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def make_response_item(role, text, *, text_type, phase="final_answer"):
    return {
        "type": "response_item",
        "payload": {
            "type": "message",
            "role": role,
            "phase": phase,
            "content": [{"type": text_type, "text": text}],
        },
    }


def make_user_message(text):
    return {
        "type": "event_msg",
        "payload": {
            "type": "user_message",
            "message": text,
        },
    }


class StopCheckerStateTests(unittest.TestCase):
    def write_transcript(self, events):
        handle = tempfile.NamedTemporaryFile("w", delete=False)
        try:
            for event in events:
                handle.write(json.dumps(event) + "\n")
            return handle.name
        finally:
            handle.close()

    def assert_state(self, events, expected):
        transcript_path = self.write_transcript(events)
        self.addCleanup(lambda: Path(transcript_path).unlink(missing_ok=True))
        self.assertEqual(MODULE.marker_active_for_thread(transcript_path), expected)

    def test_inactive_without_marker(self):
        self.assert_state([make_user_message("hello")], False)

    def test_active_after_explicit_marker(self):
        self.assert_state([make_user_message("please use $stop-checker")], True)

    def test_done_clears_state_for_later_turns(self):
        self.assert_state(
            [
                make_user_message("please use $stop-checker"),
                make_response_item(
                    "assistant",
                    (
                        "done\n"
                        "<stop_checker><status>done</status>"
                        "<reason>finished</reason>"
                        "<completion_evidence>verified</completion_evidence></stop_checker>"
                    ),
                    text_type="output_text",
                ),
            ],
            False,
        )

    def test_continue_keeps_state_active(self):
        self.assert_state(
            [
                make_user_message("please use $stop-checker"),
                make_response_item(
                    "assistant",
                    (
                        "continue\n"
                        "<stop_checker><status>continue</status>"
                        "<reason>still working</reason></stop_checker>"
                    ),
                    text_type="output_text",
                ),
            ],
            True,
        )

    def test_clear_command_disables_even_with_following_skill_injection(self):
        self.assert_state(
            [
                make_user_message("please use $stop-checker"),
                make_response_item(
                    "assistant",
                    (
                        "done\n"
                        "<stop_checker><status>done</status>"
                        "<reason>finished</reason>"
                        "<completion_evidence>verified</completion_evidence></stop_checker>"
                    ),
                    text_type="output_text",
                ),
                make_user_message("$stop-checker clear"),
                make_response_item(
                    "user",
                    "synthetic skill payload mentioning $stop-checker",
                    text_type="input_text",
                    phase="commentary",
                ),
            ],
            False,
        )

