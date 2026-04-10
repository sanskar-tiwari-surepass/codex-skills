#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ./sync-skills.sh push [--apply] [--dest PATH]
  ./sync-skills.sh pull [--apply] [--source PATH]

Modes:
  push    Sync this repo's skills/ into ~/.codex/skills and repo agents/ into ~/.codex/agents
  pull    Sync ~/.codex/skills back into repo skills/ and ~/.codex/agents into repo agents/

Behavior:
  - Dry-run by default
  - Use --apply to perform the sync
  - Uses --delete for full mirror sync
  - Preserves any .system directory on either side for both skills and agents
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
codex_root="${HOME}/.codex"
repo_skills_dir="${repo_root}/skills"
repo_agents_dir="${repo_root}/agents"
skills_dir="${codex_root}/skills"
agents_dir="${codex_root}/agents"
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
      agents_dir="$(cd "$(dirname "${skills_dir}")" && pwd)/agents"
      shift 2
      ;;
    --source)
      if [[ "${mode}" != "pull" ]]; then
        echo "--source is only valid with pull" >&2
        exit 1
      fi
      skills_dir="${2:?missing path for --source}"
      agents_dir="$(cd "$(dirname "${skills_dir}")" && pwd)/agents"
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

skills_rsync_args=(
  -avh
  --delete
  --exclude=.git/
  --exclude=.gitignore
  --exclude=.omx/
  --exclude=.DS_Store
  --exclude=agents/
  --exclude=skills/
  --exclude=.system/
  --exclude='__pycache__/'
  --exclude='*.pyc'
  --exclude='*.pyo'
  --exclude='*.pyd'
  "--exclude=${script_name}"
)

agents_rsync_args=(
  -avh
  --delete
  --exclude=.DS_Store
  --exclude=.system/
  --exclude='__pycache__/'
  --exclude='*.pyc'
  --exclude='*.pyo'
  --exclude='*.pyd'
)

if [[ "${apply}" == false ]]; then
  skills_rsync_args+=(-n)
  agents_rsync_args+=(-n)
fi

case "${mode}" in
  push)
    skills_src="${repo_skills_dir}/"
    skills_dest="${skills_dir}/"
    agents_src="${repo_agents_dir}/"
    agents_dest="${agents_dir}/"
    ;;
  pull)
    skills_src="${skills_dir}/"
    skills_dest="${repo_skills_dir}/"
    agents_src="${agents_dir}/"
    agents_dest="${repo_agents_dir}/"
    ;;
  *)
    echo "Unknown mode: ${mode}" >&2
    usage
    exit 1
    ;;
esac

run_sync() {
  local label="$1"
  local src="$2"
  local dest="$3"
  shift 3
  local -a args=("$@")

  if [[ ! -d "${src%/}" ]]; then
    echo "Skipping ${label}: source directory not found: ${src%/}"
    return 0
  fi

  if ! find "${src%/}" \
    -mindepth 1 \
    -not -path '*/.system/*' \
    -not -name '.system' \
    -not -path '*/__pycache__/*' \
    -not -name '__pycache__' \
    -not -name '*.pyc' \
    -not -name '*.pyo' \
    -not -name '*.pyd' \
    | read -r _; then
    echo "Skipping ${label}: source directory has no syncable content: ${src%/}"
    return 0
  fi

  if [[ "${apply}" == true ]]; then
    mkdir -p "${dest%/}"
  fi

  echo "${label}:"
  echo "  Source: ${src}"
  echo "  Destination: ${dest}"
  rsync "${args[@]}" "${src}" "${dest}"
}

echo "Mode: ${mode}"
if [[ "${apply}" == false ]]; then
  echo "Dry run: yes"
else
  echo "Dry run: no"
fi
echo

run_sync "Skills sync" "${skills_src}" "${skills_dest}" "${skills_rsync_args[@]}"
echo
run_sync "Agents sync" "${agents_src}" "${agents_dest}" "${agents_rsync_args[@]}"
