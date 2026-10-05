#!/usr/bin/env bash
set -euo pipefail

# work(또는 지정한 소스 브랜치)에서 fork 전용 인프라 파일을 제거한 임시 브랜치를
# 만들어 push하고, 그 브랜치로 업스트림(eGovFramework/egovframe-docs) main에
# PR을 연다. 원본 소스 브랜치는 그대로 남아있다.
#
# PR 제목/본문은 지정하지 않는다 — gh pr create가 대화형으로 물어본다.
#
# 사용법: scripts/open_upstream_pr.sh [source-branch=work]

SRC="${1:-work}"
UPSTREAM_REPO="eGovFramework/egovframe-docs"
CLEAN_BRANCH="upstream-submit/$(date +%Y%m%d%H%M%S)"

# 업스트림으로 절대 보내면 안 되는 fork 전용 인프라 파일 목록.
# 이 스크립트 자신과 sync-upstream-main.yml도 fork 전용이라 포함한다.
DENYLIST=(
  ".github/FORK_PREVIEW.md"
  ".github/workflows/fork-preview.yml"
  ".github/workflows/sync-upstream-main.yml"
  "scripts/prepare_fork_site.py"
  "scripts/preview_fork.sh"
  "scripts/open_upstream_pr.sh"
)

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

git fetch origin "$SRC"
git checkout -B "$CLEAN_BRANCH" "origin/$SRC"

removed=()
for f in "${DENYLIST[@]}"; do
  if [ -e "$f" ]; then
    git rm -rq "$f"
    removed+=("$f")
  fi
done

if [ ${#removed[@]} -gt 0 ]; then
  printf '다음 fork 전용 파일을 제거했습니다:\n'
  printf '  - %s\n' "${removed[@]}"
  git commit -m "chore: strip fork-only tooling before upstream submission"
else
  echo "제거할 fork 전용 파일이 없습니다 (이미 없음)."
fi

git push -u origin "$CLEAN_BRANCH"

gh pr create --repo "$UPSTREAM_REPO" --base main --head "leejongyoung:$CLEAN_BRANCH"

echo
echo "원본 브랜치($SRC)는 그대로 유지됩니다. 임시 제출 브랜치: $CLEAN_BRANCH"
