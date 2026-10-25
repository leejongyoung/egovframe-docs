# egovframe-docs project context

Observed from the `work` source at `2a3fe33361b21b19eea0252b9ba78ee86c8df5ae` on 2026-10-26.
This is a maintenance context card, not a claim that application checks were run during adoption.

## Role and public entry points

Markdown guide content for the eGovFrame portal: `common-component/`, `egovframe-development/` and `egovframe-runtime/`. The site generator/theme lives in a separate orphan `hugo-project` history; it is not an application or theme tree inside this work checkout.

## Evidence and maintenance boundaries

- `README.md`: content layout, writing/links/image conventions, guide entry points.
- `AGENTS.md`: independent histories, frontmatter/menu restrictions, pinned preview, full-site diff and browser verification requirements.
- `.github/workflows/fork-preview.yml`: content/theme assembly and Hugo 0.167.0 build; work content uploads an artifact, theme track publishes.
- `scripts/prepare_fork_site.py`, `scripts/preview_fork.sh`: local assembly and preview behavior.
- `docs_lint.md`, `.github/workflows/markdown-lint.yml`, `.github/workflows/link-check.yml`: local checker versus disabled workflows.
- Existing PR descriptions in AGENTS are historical; query current PR state instead of assuming they remain open.

Keep the change scope and workflow policy in the [constitution](constitution.md); concept cards
link there rather than repeating the policy. Author a concept card only for actual planned work.

## Build and verification commands

- Local preview: `./scripts/preview_fork.sh`, with fetched origin/hugo-project and verified Hugo extended 0.167.0. It serves the assembled site at localhost:8888.
- CI assembly: Python `scripts/prepare_fork_site.py <docs> <site>`, then `hugo --source site --destination <output> --minify`. Use `uv run scripts/prepare_fork_site.py ...` when invoking Python in this workspace.
- Local targeted consistency: `uv run scripts/docs_lint.py common-component` (or affected content directory), optional --src for actual source-reference checks. It is not enabled in CI.
- Theme/Hugo changes require baseline/output page-by-page comparison; client diagram behavior additionally needs browser verification. Adoption did not build the site or claim browser/link-check success.

For this tooling-only adoption, verify Spec Kit CLI/integration status, installed core/bug commands,
constitution completeness, and template resolution/scaffold presence. Full application build,
lint, tests, formatter, external services, and deployment are not part of that smoke check.

## Upstream and submission baseline

Actual upstream is eGovFramework/egovframe-docs, default main. The fetched main SHA is the submission baseline. Existing upstream-submit/* branches and PRs occupy the Git namespace, so a bare remote upstream-submit cannot coexist and is not created; preserve the submission family without deletion, rename or alternate ref. The local bare branch records the upstream base only. This does not cover the independent hugo-project history; a future theme contribution must establish its own actual upstream theme base and dependencies.

Use a separate Orca submission worktree from the fetched upstream base. Preserve existing PR heads and `upstream-submit/*` disposable-head policy. The current work-derived `scripts/open_upstream_pr.sh` does not establish clean upstream history and its denylist predates Spec Kit; do not use it for this new isolation workflow. Transfer only selected content/test/user-doc patches to the clean base and inspect the full diff and commits, without copying tooling or model cards.
No PR is created by adoption. Do not merge `work` or cherry-pick its adoption commit into a submission.
Preserve existing submission branches and PRs. Inspect changed paths and commits against the exact
base before any later PR; exclude work-only scaffolding without deleting upstream-owned files.

## Working with the pinned tooling

Installed by `uvx --from specify-cli==1.2.3 specify init --here --force --non-interactive
--integration omp --script sh --extension bug` after checking for existing path conflicts.
The CLI's init metadata pins 1.2.3; native agent commands live in `.omp/commands/`, including
`speckit.bug.assess.md`, `speckit.bug.fix.md`, and `speckit.bug.test.md`.
Use official upgrade support for future changes and preserve local customizations.
The new [domain model card template](../templates/model-card-template.md) aligns concept meanings
before specification; it is not an ML performance or benchmark card.

Observed submission base: `94ce018e817fa2bddde6aad3a02cbefeca8afcda` (eGovFramework/egovframe-docs, `main`).
Submission branch status: preserved-existing-upstream-submit-family; bare remote ref blocked by Git namespace collision.
