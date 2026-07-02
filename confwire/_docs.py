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
