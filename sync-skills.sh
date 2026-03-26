#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ./sync-skills.sh push [--apply] [--dest PATH]
  ./sync-skills.sh pull [--apply] [--source PATH]

Modes:
  push    Sync this repo into ~/.codex/skills
  pull    Sync ~/.codex/skills back into this repo

Behavior:
  - Dry-run by default
  - Use --apply to perform the sync
  - Uses --delete for full mirror sync
  - Preserves any .system directory on either side
  - Excludes this repo's .git directory

Examples:
  ./sync-skills.sh push
  ./sync-skills.sh push --apply
  ./sync-skills.sh pull
  ./sync-skills.sh pull --apply
EOF
}

mode="${1:-}"
if [[ "${mode}" == "-h" || "${mode}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ -z "${mode}" ]]; then
  usage
  exit 1
fi
shift || true

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
script_name="$(basename "${BASH_SOURCE[0]}")"
skills_dir="${HOME}/.codex/skills"
apply=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply)
      apply=true
      shift
      ;;
    --dest)
      if [[ "${mode}" != "push" ]]; then
        echo "--dest is only valid with push" >&2
        exit 1
      fi
      skills_dir="${2:?missing path for --dest}"
      shift 2
      ;;
    --source)
      if [[ "${mode}" != "pull" ]]; then
        echo "--source is only valid with pull" >&2
        exit 1
      fi
      skills_dir="${2:?missing path for --source}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ ! -d "${skills_dir}" ]]; then
  echo "Skills directory not found: ${skills_dir}" >&2
  exit 1
fi

rsync_args=(
  -avh
  --delete
  --exclude=.git/
  --exclude=.system/
  --exclude='__pycache__/'
  --exclude='*.pyc'
  --exclude='*.pyo'
  --exclude='*.pyd'
  "--exclude=${script_name}"
)

if [[ "${apply}" == false ]]; then
  rsync_args+=(-n)
fi

case "${mode}" in
  push)
    src="${repo_root}/"
    dest="${skills_dir}/"
    ;;
  pull)
    src="${skills_dir}/"
    dest="${repo_root}/"
    ;;
  *)
    echo "Unknown mode: ${mode}" >&2
    usage
    exit 1
    ;;
esac

echo "Mode: ${mode}"
echo "Source: ${src}"
echo "Destination: ${dest}"
if [[ "${apply}" == false ]]; then
  echo "Dry run: yes"
else
  echo "Dry run: no"
fi

rsync "${rsync_args[@]}" "${src}" "${dest}"
