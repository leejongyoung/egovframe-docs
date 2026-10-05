#!/usr/bin/env python3
"""Close this fork's issues once their linked upstream PRs have all merged.

An issue is closed only when BOTH hold:
  1. Every markdown checkbox in its body is checked (`- [x]`), or it has no
     checkboxes at all (some issues, e.g. the broken-submodule one, are pure
     prose with no checklist).
  2. At least one upstream PR URL
     (github.com/eGovFramework/egovframe-docs/pull/<N>) appears somewhere in
     the issue body or its comments, and every PR number found that way is
     in the MERGED state.

Both conditions matter: an issue can have an unmerged-but-linked PR (not
done yet) or a merged PR that only resolved part of a still-open checklist
(see issue #11 -- #1151 merging must not auto-close it while the
locale/direction items remain unchecked). Requiring both avoids closing an
issue on a partial fix.
"""

from __future__ import annotations

import json
import re
import subprocess

FORK = "leejongyoung/egovframe-docs"
UPSTREAM = "eGovFramework/egovframe-docs"
PR_URL_RE = re.compile(rf"github\.com/{re.escape(UPSTREAM)}/pull/(\d+)")
CHECKBOX_RE = re.compile(r"^- \[([ x])\]", re.MULTILINE)


def gh_json(args: list[str]):
    result = subprocess.run(["gh", *args], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def main() -> None:
    issues = gh_json(
        ["issue", "list", "--repo", FORK, "--state", "open", "--json", "number,body"]
    )

    for issue in issues:
        number = issue["number"]
        body = issue["body"] or ""

        checkbox_states = CHECKBOX_RE.findall(body)
        if any(state == " " for state in checkbox_states):
            continue  # checklist not fully done yet

        comments = gh_json(
            ["issue", "view", str(number), "--repo", FORK, "--json", "comments", "-q", ".comments"]
        )
        full_text = body + "\n" + "\n".join(c["body"] for c in comments)
        pr_numbers = sorted({int(m) for m in PR_URL_RE.findall(full_text)})
        if not pr_numbers:
            continue  # no upstream PR linked yet

        states = {}
        for pr in pr_numbers:
            pr_info = gh_json(["pr", "view", str(pr), "--repo", UPSTREAM, "--json", "state"])
            states[pr] = pr_info["state"]

        # A PR that was closed without merging (e.g. superseded by a fresh
        # PR, as #1149 was by #1151) carries no information about whether
        # the issue is resolved -- drop it instead of letting a dead
        # reference block this issue forever.
        live_states = {pr: s for pr, s in states.items() if s != "CLOSED"}
        if not live_states:
            continue

        if all(state == "MERGED" for state in live_states.values()):
            pr_list = ", ".join(f"#{pr}" for pr in live_states)
            subprocess.run(
                [
                    "gh", "issue", "close", str(number), "--repo", FORK,
                    "--comment",
                    f"연결된 업스트림 PR이 모두 머지되었습니다 ({pr_list}). "
                    "체크리스트도 전부 완료되어 자동으로 닫습니다.",
                ],
                check=True,
            )
            print(f"closed #{number} (resolved by {pr_list})")
        else:
            pending = [f"#{pr}({s})" for pr, s in live_states.items() if s != "MERGED"]
            print(f"#{number}: checklist complete, still waiting on {', '.join(pending)}")


if __name__ == "__main__":
    main()
