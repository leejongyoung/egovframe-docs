# Fork preview

This fork keeps `main` aligned with the upstream repository. Work on a topic branch,
open a pull request with `leejongyoung/egovframe-docs:work` as its base, and review
the generated HTML artifact in the **Fork Hugo preview** workflow.

After the pull request is merged into `work`, the same workflow builds that branch
with the fork's `hugo-project` branch, updates the fork's `gh-pages` branch, and
publishes the result at <https://leejongyoung.github.io/egovframe-docs/>. These
steps use only branches and GitHub Pages belonging to this fork.

For an immediate local preview, install Hugo 0.139.0 and run:

```sh
./scripts/preview_fork.sh
```

The script renders the current checkout, including uncommitted document changes,
at <http://127.0.0.1:8888/>, using the Hugo layout from `origin/hugo-project`.
