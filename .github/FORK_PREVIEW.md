# Fork preview

See [`AGENTS.md`](../AGENTS.md) at the repo root for the full branch model
(two tracks, four branch roles), the fork-first PR workflow, and the
upstream-submission script. This file is a quick reference for the content
track specifically.

`main` is a pure mirror of upstream `main`, kept in sync by
`.github/workflows/sync-upstream-mirrors.yml` (daily + manual
`workflow_dispatch`, fast-forward only). Work on `work` instead, and review
changes via the **Fork Hugo preview** workflow, which builds an HTML
artifact on every push/PR to `work`. Pushes to `work` additionally publish
to this fork's own `gh-pages` branch and GitHub Pages at
<https://leejongyoung.github.io/egovframe-docs/> — these steps only ever
touch branches and Pages belonging to this fork.

For an immediate local preview, install Hugo 0.139.0 (extended) and run:

```sh
./scripts/preview_fork.sh
```

This renders the current checkout, including uncommitted document changes,
at <http://127.0.0.1:8888/>, using the Hugo layout from `origin/hugo-project`.

When `work` is ready for `eGovFramework/egovframe-docs`, run
`scripts/open_upstream_pr.sh work main` — see `AGENTS.md` for what it does
and the full fork-only-file denylist.
