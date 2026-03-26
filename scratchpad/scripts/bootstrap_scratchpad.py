#!/usr/bin/env python3
"""Create a per-repo .scratchpad/ scaffold and default ignore rule."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

IGNORE_ENTRY = ".scratchpad/"
IGNORE_COMMENT = "# scratchpad skill"

FILES = {
    "index.md": """# Scratchpad

Use this folder for durable repo memory. Keep it concise and easy to scan.

## Files

- `preferences.md`: user and team preferences that affect repeated work
- `patterns.md`: commands, workflows, and conventions that repeatedly work
- `pitfalls.md`: recurring mistakes, gotchas, and failure modes
- `active.md`: live context worth carrying into nearby sessions

## Rules

- Prefer durable guidance over session history.
- Rewrite and merge notes instead of stacking duplicates.
- Keep notes in Markdown.
- Remove stale notes when they stop helping.
""",
    "preferences.md": """# Preferences

## User Preferences

- Add durable preferences here.

## Team Conventions

- Add stable team or repo conventions here.
""",
    "patterns.md": """# Patterns

## Reliable Commands

- Add commands and validation steps that repeatedly work.

## Workflow Patterns

- Add reusable repo-specific workflow guidance here.
""",
    "pitfalls.md": """# Pitfalls

## Recurring Gotchas

- Add repeated failure modes and how to avoid them.

## Bad Assumptions To Avoid

- Add assumptions that keep proving wrong in this repo.
""",
    "active.md": """# Active Context

## Current Focus

- Add short-lived context that should survive into the next few sessions.

## Open Questions

- Add unresolved questions that matter to ongoing work.
""",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a .scratchpad/ scaffold in a repository.",
    )
    parser.add_argument(
        "--repo",
        help="Repository root. Defaults to the git root for the current directory, or cwd if not in git.",
    )
    return parser.parse_args()


def resolve_repo_root(repo_arg: str | None) -> Path:
    if repo_arg:
        return Path(repo_arg).expanduser().resolve()

    git_root = discover_git_root()
    if git_root is not None:
        return git_root

    return Path.cwd().resolve()


def discover_git_root() -> Path | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None

    root = result.stdout.strip()
    if not root:
        return None
    return Path(root).resolve()


def ensure_repo_exists(repo_root: Path) -> None:
    if not repo_root.exists():
        raise SystemExit(f"Repository path does not exist: {repo_root}")
    if not repo_root.is_dir():
        raise SystemExit(f"Repository path is not a directory: {repo_root}")


def ensure_scratchpad(repo_root: Path) -> tuple[Path, bool]:
    scratchpad_dir = repo_root / ".scratchpad"
    existed = scratchpad_dir.exists()
    scratchpad_dir.mkdir(parents=True, exist_ok=True)

    for name, contents in FILES.items():
        path = scratchpad_dir / name
        if not path.exists():
            path.write_text(contents)

    return scratchpad_dir, existed


def has_ignore_entry(text: str) -> bool:
    entries = {line.strip() for line in text.splitlines()}
    return IGNORE_ENTRY in entries or f"/{IGNORE_ENTRY}" in entries


def ensure_gitignore(repo_root: Path, scratchpad_already_existed: bool) -> bool:
    if scratchpad_already_existed:
        return False

    gitignore_path = repo_root / ".gitignore"
    existing = gitignore_path.read_text() if gitignore_path.exists() else ""

    if has_ignore_entry(existing):
        return False

    addition = f"{IGNORE_COMMENT}\n{IGNORE_ENTRY}\n"
    if existing and not existing.endswith("\n"):
        addition = "\n" + addition

    gitignore_path.write_text(existing + addition)
    return True


def main() -> int:
    args = parse_args()
    repo_root = resolve_repo_root(args.repo)
    ensure_repo_exists(repo_root)

    scratchpad_dir, existed = ensure_scratchpad(repo_root)
    gitignore_updated = ensure_gitignore(repo_root, existed)

    print(f"repo={repo_root}")
    print(f"scratchpad={scratchpad_dir}")
    print(f"created={'no' if existed else 'yes'}")
    print(f"gitignore_updated={'yes' if gitignore_updated else 'no'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
