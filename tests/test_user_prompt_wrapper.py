import importlib.util
import io
import json
import unittest
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).resolve().parents[1] / "hooks" / "user_prompt_wrapper.py"
SPEC = importlib.util.spec_from_file_location("user_prompt_wrapper", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class UserPromptWrapperTests(unittest.TestCase):
    def test_build_wrapped_prompt_marks_latest_prompt(self):
        wrapped = MODULE.build_wrapped_prompt(
            "ship <now> & don't break </prompt>",
            submitted_at_utc="2026-04-14T12:34:56Z",
        )

        self.assertIn("Use the prompt with the newest timestamp", wrapped)
        self.assertIn('<prompt timestamp="2026-04-14T12:34:56Z">', wrapped)
        self.assertIn("ship &lt;now&gt; &amp; don't break &lt;/prompt&gt;</prompt>", wrapped)

    def test_main_wraps_user_prompt_submit_payload(self):
        payload = {
            "hook_event_name": "UserPromptSubmit",
            "prompt": "latest request",
        }

        stdin = io.StringIO(json.dumps(payload))
        stdout = io.StringIO()

        with patch("sys.stdin", stdin), patch("sys.stdout", stdout):
            result = MODULE.main()

        self.assertEqual(result, 0)
        rendered = stdout.getvalue()
        self.assertIn("<instruction>", rendered)
        self.assertIn("<prompt timestamp=", rendered)
        self.assertIn(">latest request</prompt>", rendered)

    def test_main_ignores_non_prompt_events(self):
        payload = {
            "hook_event_name": "Stop",
            "prompt": "ignored",
        }

        stdin = io.StringIO(json.dumps(payload))
        stdout = io.StringIO()

        with patch("sys.stdin", stdin), patch("sys.stdout", stdout):
            result = MODULE.main()

        self.assertEqual(result, 0)
        self.assertEqual(stdout.getvalue(), "")

    def test_main_ignores_missing_prompt(self):
        payload = {
            "hook_event_name": "UserPromptSubmit",
            "prompt": "",
        }

        stdin = io.StringIO(json.dumps(payload))
        stdout = io.StringIO()

        with patch("sys.stdin", stdin), patch("sys.stdout", stdout):
            result = MODULE.main()

        self.assertEqual(result, 0)
        self.assertEqual(stdout.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
