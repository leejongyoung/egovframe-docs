#!/usr/bin/env bash
set -euo pipefail

# 소스 브랜치(기본 트랙 통합 브랜치 work 또는 work-hugo-project)에서
# fork 전용 인프라 파일을 제거한 임시 브랜치를 만들어 push하고, 그 브랜치로
# 업스트림(eGovFramework/egovframe-docs)의 지정한 base 브랜치에 PR을 연다.
# 원본 소스 브랜치는 그대로 남아있다.
#
# 반드시 소스/base 브랜치 쌍을 직접 지정한다(자동 추측하지 않음):
#   work              -> main          (문서/콘텐츠 트랙)
#   work-hugo-project -> hugo-project  (Hugo 테마 트랙)
#
# PR 제목/본문은 지정하지 않는다 — gh pr create가 대화형으로 물어본다.
#
# 사용법: scripts/open_upstream_pr.sh <source-branch> <upstream-base-branch>
# 예시:   scripts/open_upstream_pr.sh work main
#         scripts/open_upstream_pr.sh work-hugo-project hugo-project

if [ $# -ne 2 ]; then
  echo "usage: $0 <source-branch> <upstream-base-branch>" >&2
  echo "  예: $0 work main" >&2
  echo "      $0 work-hugo-project hugo-project" >&2
  exit 1
fi

SRC="$1"
BASE="$2"
UPSTREAM_REPO="eGovFramework/egovframe-docs"
CLEAN_BRANCH="upstream-submit/$(date +%Y%m%d%H%M%S)"

# 업스트림으로 절대 보내면 안 되는 fork 전용 인프라 파일 목록.
# 두 트랙(work, work-hugo-project) 전체를 아우르는 superset이다 —
# 각 파일은 해당하는 트랙에만 존재하므로 다른 트랙에서는 "없으면 건너뜀"으로 처리된다.
DENYLIST=(
  "AGENTS.md"
  ".github/FORK_PREVIEW.md"
  ".github/workflows/fork-preview.yml"
  ".github/workflows/sync-upstream-mirrors.yml"
  ".github/workflows/close-resolved-issues.yml"
  "scripts/prepare_fork_site.py"
  "scripts/preview_fork.sh"
  "scripts/open_upstream_pr.sh"
  "scripts/close_resolved_issues.py"
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

gh pr create --repo "$UPSTREAM_REPO" --base "$BASE" --head "leejongyoung:$CLEAN_BRANCH"

echo
echo "원본 브랜치($SRC)는 그대로 유지됩니다. 임시 제출 브랜치: $CLEAN_BRANCH"
