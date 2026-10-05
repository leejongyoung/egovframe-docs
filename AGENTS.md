# AGENTS.md

Instructions for AI coding agents (Claude Code, Codex, Copilot, etc.) working in
**leejongyoung/egovframe-docs**, a personal fork of
[eGovFramework/egovframe-docs](https://github.com/eGovFramework/egovframe-docs)
used to prepare clean contributions back to that upstream repo.

This file is fork-only tooling: it must never be sent upstream (see
"Submitting to upstream" below). If you are reading this while checked out on
`main` or `hugo-project`, something is wrong — those branches must stay
byte-identical to upstream.

## Mental model: two tracks, four branch roles

Upstream has two unrelated histories: `main` (Markdown content) and
`hugo-project` (an orphan branch holding the Hugo site generator + the
`krds-theme` theme). This fork mirrors that split and adds one integration
branch per track:

| Branch              | Role                                                             | Who commits here |
|----------------------|-------------------------------------------------------------------|-------------------|
| `main`               | Byte-identical mirror of upstream `main`                          | Bot only (fast-forward) |
| `work`               | **Default branch.** Content-track dev/integration + fork tooling  | You |
| `hugo-project`       | Byte-identical mirror of upstream `hugo-project`                  | Bot only (fast-forward) |
| `work-hugo-project`  | Theme-track dev/integration branch, branched from `hugo-project`  | You |
| `gh-pages`           | Generated build output                                            | Nobody — never hand-edit |

**Why `main`/`hugo-project` must stay pure:** GitHub Actions `schedule`
(cron) triggers are only evaluated from the workflow file as it exists on the
repository's **default branch**. The default branch was moved to `work` for
exactly this reason — it lets `main` and `hugo-project` stay untouched
mirrors while the daily sync automation (`.github/workflows/sync-upstream-mirrors.yml`,
cron `0 15 * * *` UTC + manual `workflow_dispatch`) lives on `work` and
fast-forwards both mirrors from upstream. The merge is `--ff-only`: if either
mirror ever diverges (e.g. someone commits to it directly), the sync job
fails loudly instead of silently force-pushing. **Never commit directly to
`main` or `hugo-project`.**

## The fork-first PR workflow

Always land changes on this fork before they go upstream — never open a PR
against `eGovFramework/egovframe-docs` directly from a throwaway branch.

1. Branch from the relevant mirror:
   - Content/docs change → branch from `main`.
   - Theme/Hugo change → branch from `hugo-project`.
2. Open a PR **against this fork's own integration branch** (`work` or
   `work-hugo-project`). This is the review checkpoint — CI (`fork-preview.yml`)
   builds the site and uploads a downloadable HTML preview artifact on every
   push/PR to either integration branch. Use this step for agent review,
   human review, or both, before anything goes near upstream.
3. **Default cadence: batch, don't submit after every single fork PR.** Let
   several fork-side PRs land on `work`/`work-hugo-project` first, then cut
   *one* upstream submission covering all of them. Submitting upstream
   immediately after each individual fork PR merge (as was done once for
   PRs [#1149](https://github.com/eGovFramework/egovframe-docs/pull/1149)
   and [#1150](https://github.com/eGovFramework/egovframe-docs/pull/1150))
   is the exception, not the rule — upstream reviewers deal with one
   consolidated PR per batch, not a stream of small ones. Either way, the
   script below only runs when a human chooses to run it — nothing in this
   repo opens PRs against the upstream repo automatically.

### Submitting to upstream

```sh
scripts/open_upstream_pr.sh work main                    # content track
scripts/open_upstream_pr.sh work-hugo-project hugo-project # theme track
```

This creates a disposable `upstream-submit/<timestamp>` branch from the given
source, **strips the fork-only tooling denylist** (see the `DENYLIST` array
inside the script — currently `AGENTS.md`, `.github/FORK_PREVIEW.md`,
`.github/workflows/fork-preview.yml`, `.github/workflows/sync-upstream-mirrors.yml`,
`scripts/prepare_fork_site.py`, `scripts/preview_fork.sh`,
`scripts/open_upstream_pr.sh`), pushes it, and opens a PR against
`eGovFramework/egovframe-docs` with `gh pr create` (title/body are entered
interactively). The source branch (`work`/`work-hugo-project`) is left
untouched. **If you add new fork-only files, add them to `DENYLIST` first.**

## Upstream rules you must not break

- **Never touch the frontmatter of an existing `.md` file** on the content
  track. Upstream's `merge-on-pr.yaml` bot diffs frontmatter blocks (the
  first `---`…`---`) on every PR touching `main`; if it detects a change on
  a *modified* file (new files are exempt), it blocks auto-merge and comments
  on the PR asking for maintainer review. Add new files without frontmatter
  and describe their menu placement in the PR template's "추가 참고 사항" field
  instead.
- **2026 contribution scope is `common-component/` (primary), plus
  `egovframe-development/` and `egovframe-runtime/`.** New top-level menus
  are explicitly not accepted upstream.
- `hugo-project` has **no `.github/workflows/` directory of its own** — all
  CI for building/deploying the site lives in `main`'s workflows
  (`deploy-on-merge.yaml`, `deploy-on-push.yaml`, `deploy-on-schedule.yaml`)
  and this fork's `fork-preview.yml`. A fix that only touches a workflow
  YAML's settings (e.g. the pinned Hugo version) belongs on the content
  track (`main`/`work`), not a `hugo-project` PR, even if it's about
  building the Hugo site.
- `hugo-project` commit history so far is maintainer-only accounts
  (`hjlee1107`, `eGovFrameSupport`). Treat changes there as proposals, not
  assumed-acceptable PRs.

## Local preview

```sh
./scripts/preview_fork.sh
```

Renders the current checkout (including uncommitted changes) at
`http://127.0.0.1:8888/`, using the Hugo layout from `origin/hugo-project`
and the pinned Hugo **0.167.0** (extended) binary — match this version
exactly when testing locally; a different Hugo version is not a valid test
of what CI will do. `scripts/prepare_fork_site.py` is what rewrites
`hugo.toml`'s baseURL/repo links from the upstream site to
`leejongyoung.github.io` for both the local script and CI; look there before
changing any URL-rewriting logic.

The live fork preview (pushes to `work` only) is published at
<https://leejongyoung.github.io/egovframe-docs/>.

## Verifying a change before opening any PR

There's no CI step on this fork that actually builds the full site with
real content and diffs it — do this manually:

```sh
# Linux/CI-matching binary: download the exact pinned version, don't use
# whatever `hugo` happens to be on PATH.
gh release download v0.167.0 --repo gohugoio/hugo \
  --pattern "hugo_extended_0.167.0_Linux-64bit.tar.gz"

# macOS: recent Hugo releases only ship a .pkg installer for darwin, not a
# tarball. `brew install hugo` is the simplest way to get the matching
# version locally (Homebrew's hugo formula tracks latest stable) - just
# confirm with `hugo version` that it matches the pin before trusting a
# diff.
brew install hugo && hugo version
```

Then build with real `main` content copied into `hugo-project`'s `content/`
(mirroring what CI's "Copy markdown files to content" step does), and diff
the output `public/` tree against a baseline build from before your change.
A change that touches the theme should produce a **page-by-page diff you can
fully explain** — if pages differ in ways you didn't intend, stop and
investigate before opening a PR. This is how the three `hugo-project` fixes
in PR [#1149](https://github.com/eGovFramework/egovframe-docs/pull/1149)
were verified (708/708 pages, only the intended footer-year line differed).

## Known gotchas (so you don't rediscover them)

- **`krds-theme` is not really a git submodule.** `.gitmodules` used to
  declare it as one, but the tree entry was always a plain directory (mode
  `040000`, not a commit gitlink `160000`) on both the fork and upstream —
  `git submodule update --init` was a silent no-op. The stale `.gitmodules`
  was removed in PR #1149; the theme is just a vendored directory.
- **The merged `custom.js`'s SRI `integrity` attribute is empty** (see
  `themes/krds-theme/layouts/partials/head/js.html`, the `resources.Concat`
  output). This is a pre-existing upstream bug unrelated to anything this
  fork has changed — don't assume you broke it if you see it, and don't try
  to "fix" it incidentally as part of an unrelated change.
- **`mermaid.min.js` is vendored with no `package.json`.** It's mermaid's
  own official `dist/mermaid.min.js` npm build (confirmed by the matching
  esbuild wrapper shape), just copied in without any version marker.
  Currently `12.1.0` (bumped from a buried `version:"11.15.0"` string found
  inside the obfuscated 11.x source) — check
  `gh api repos/mermaid-js/mermaid/tags` before assuming this is still
  current. The header comment records the version; keep it updated if you
  bump the bundle again, and re-verify rendering the same way PR #1149 did
  (Playwright + real Chrome against every diagram type actually used in
  `main`'s content, not just a build-succeeds check — mermaid renders
  client-side, so a clean Hugo build proves nothing about whether diagrams
  still draw correctly).
- **The Hugo version pin was bumped `0.139.0` → `0.167.0`** (fork issue
  [#6](https://github.com/leejongyoung/egovframe-docs/issues/6), upstream PR
  [#1150](https://github.com/eGovFramework/egovframe-docs/pull/1150)). Don't
  bump it again casually; it needs the same before/after full-site-diff
  verification described above. 0.167.0 also surfaces three new deprecation
  warnings that only matter for `hugo-project` (its `hugo.toml`'s
  `languageCode` key, and `.Language.LanguageCode`/`.Language.LanguageDirection`
  in templates, plus an "unrecognized render hook template" warning for an
  already-dead template) — tracked separately as a `hugo-project`/
  `work-hugo-project` fix, not a content-track one.
- **`markdown-lint.yml` and `link-check.yml` on `main` are entirely commented
  out** — they do nothing. `scripts/docs_lint.py` exists but is not wired
  into any CI workflow either. Don't assume either one is actually linting
  anything right now.
- **`deploy-on-*.yaml` on `main` install Node.js 18** (EOL since 2025-04)
  even though the Hugo build itself needs no Node tooling that's visible in
  this repo. Not yet filed as an issue — if you investigate and find it's
  genuinely dead weight, file one.

## Issue/label/milestone conventions on this fork

Labels use a two-axis scheme, `type:*` (what kind of change) × `area:*`
(which part of the repo) — e.g. `type:docs`, `type:update`,
`type:maintenance`, `type:research`, `area:common-component`,
`area:development`, `area:runtime`, `area:infra`, `area:hugo-theme`. Default
GitHub labels (`bug`, `enhancement`, `good first issue`, ...) were
deliberately deleted in favor of this scheme — don't recreate them.

Milestones group issues by concrete, verified gaps (not aspirational
roadmap items) — e.g. "공통컴포넌트 공백 보완", "5.x 버전 정합성 점검",
"hugo-project 유지보수 점검". When filing a new issue, attach it to an
existing milestone if it fits, and add it to the GitHub Project
("egovframe-docs 기여 로드맵", project number 3, owner `leejongyoung`) with:

```sh
gh project item-add 3 --owner leejongyoung --url <issue-url>
```

Every issue should describe a finding you've actually verified (grep output,
a build log, a diff) — not a suspicion. If investigation shows an issue
can't actually be fixed in the PR scope you assumed (as happened with issue
#6 above), say so in the issue/PR rather than forcing it in anyway.

## Spec-driven workflow (lightweight, no extra tooling)

This fork doesn't install [github/spec-kit](https://github.com/github/spec-kit)
or any `.specify/` scaffolding — just follow its shape manually for any
nontrivial change:

1. **Specify** — before touching files, write (or confirm) a GitHub issue
   with a concrete, falsifiable problem statement, not a vague "improve X".
2. **Plan** — note how you'll verify the fix *before* implementing it (which
   command, which diff, which build). Decide this before writing code so you
   don't rationalize a weak verification after the fact.
3. **Implement** — make the smallest change that satisfies the plan.
4. **Verify & record** — actually run the verification from step 2, and put
   the result in the PR description (see PR #1149's "검증" section for the
   expected level of detail: exact command, exact before/after comparison).

If a step reveals the original plan doesn't work (e.g. "this needs a
different base branch," "this file doesn't exist where I assumed"), stop and
re-specify rather than forcing the original plan through.
