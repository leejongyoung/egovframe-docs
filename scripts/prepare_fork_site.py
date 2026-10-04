#!/usr/bin/env python3
"""Assemble this fork's Hugo preview without changing the Hugo source branch."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path


UPSTREAM_REPO = "https://github.com/eGovFramework/egovframe-docs"
FORK_REPO = "https://github.com/leejongyoung/egovframe-docs"
UPSTREAM_SITE = "https://eGovFramework.github.io/egovframe-docs/"
FORK_SITE = "https://leejongyoung.github.io/egovframe-docs/"


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: prepare_fork_site.py <docs-directory> <hugo-directory>")

    docs = Path(sys.argv[1]).resolve()
    site = Path(sys.argv[2]).resolve()
    config = site / "hugo.toml"
    if not config.is_file() or not docs.is_dir():
        raise SystemExit("documentation directory or Hugo configuration is missing")
    if site == docs or docs in site.parents:
        raise SystemExit("the Hugo directory must be outside the documentation directory")

    content = site / "content"
    if content.exists():
        shutil.rmtree(content)
    shutil.copytree(
        docs,
        content,
        ignore=shutil.ignore_patterns(".git", ".github", "__pycache__", ".DS_Store"),
    )

    settings = config.read_text(encoding="utf-8")
    for old, new in ((UPSTREAM_SITE, FORK_SITE), (UPSTREAM_REPO, FORK_REPO)):
        if old not in settings:
            raise SystemExit(f"expected Hugo setting not found: {old}")
        settings = settings.replace(old, new)
    settings = settings.replace(
        "https://egovframework.github.io/egovframe-docs/", FORK_SITE
    )
    config.write_text(settings, encoding="utf-8")

    footer = site / "themes/krds-theme/layouts/partials/footer.html"
    if footer.is_file():
        footer.write_text(
            footer.read_text(encoding="utf-8").replace(UPSTREAM_REPO, FORK_REPO),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
