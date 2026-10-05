# Fork preview

This fork keeps `main` as a pure mirror of the upstream repository's `main`.
All development happens on `work` instead; `main` only ever receives
fast-forward pushes from the **Sync fork main with upstream** workflow
(`.github/workflows/sync-upstream-main.yml`), which runs daily and can also
be triggered manually (`workflow_dispatch`). Because `main` is the repository's
default branch, it stays byte-identical to upstream — the sync workflow itself
lives on `work`, not on `main`.

Work on `work` (or a branch opened against `work`), and review the generated
HTML artifact in the **Fork Hugo preview** workflow. After a push to `work`,
the same workflow builds it with the fork's `hugo-project` branch, updates the
fork's `gh-pages` branch, and publishes the result at
<https://leejongyoung.github.io/egovframe-docs/>. These steps use only
branches and GitHub Pages belonging to this fork.

For an immediate local preview, install Hugo 0.139.0 and run:

```sh
./scripts/preview_fork.sh
```

The script renders the current checkout, including uncommitted document changes,
at <http://127.0.0.1:8888/>, using the Hugo layout from `origin/hugo-project`.

## Submitting to upstream

`work` carries fork-only tooling (this file, the two workflows above,
`scripts/prepare_fork_site.py`, `scripts/preview_fork.sh`, and
`scripts/open_upstream_pr.sh` itself) that must never reach the upstream
repository. When changes on `work` are ready for `eGovFramework/egovframe-docs`,
run:

```sh
./scripts/open_upstream_pr.sh
```

This creates a disposable `upstream-submit/<timestamp>` branch from `work`,
removes the fork-only paths, pushes it, and opens a PR against
`eGovFramework/egovframe-docs:main` (title/body are entered interactively via
`gh pr create`). `work` itself is left untouched. This is a manual, local step
by design — nothing in this repository opens PRs against the upstream repo
automatically.
