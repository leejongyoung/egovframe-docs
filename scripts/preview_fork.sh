#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
if ! command -v hugo >/dev/null 2>&1; then
  printf 'Hugo 0.139.0 is required for the local preview.\n' >&2
  exit 1
fi
if ! git -C "$repo_root" rev-parse --verify origin/hugo-project >/dev/null 2>&1; then
  printf 'Run git fetch origin hugo-project first.\n' >&2
  exit 1
fi

site_root="$(mktemp -d)"
trap 'rm -rf "$site_root"' EXIT
git -C "$repo_root" archive origin/hugo-project | tar -x -C "$site_root"
python3 "$repo_root/scripts/prepare_fork_site.py" "$repo_root" "$site_root"
hugo server --source "$site_root" --baseURL http://127.0.0.1:8888/ --bind 127.0.0.1 --port 8888 --disableFastRender
