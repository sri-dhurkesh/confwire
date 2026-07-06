"""Helper entry point for building the Sphinx documentation."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"


def build() -> None:
    """Build the HTML documentation via ``sphinx-build``."""
    args = sys.argv[1:] or ["-b", "html", ".", "_build/html"]
    raise SystemExit(subprocess.call(["sphinx-build", *args], cwd=DOCS_DIR))


def build_multiversion() -> None:
    """Build per-branch/tag docs via ``sphinx-multiversion`` and generate
    the versions.json used by the sphinx_material version dropdown."""
    args = sys.argv[1:] or [".", "_build/html"]
    output_dir = Path(args[-1])
    if not output_dir.is_absolute():
        output_dir = DOCS_DIR / output_dir

    ret = subprocess.call(["sphinx-multiversion", *args], cwd=DOCS_DIR)
    if ret != 0:
        raise SystemExit(ret)

    raise SystemExit(subprocess.call([sys.executable, "gen_versions_json.py", str(output_dir)], cwd=DOCS_DIR))
