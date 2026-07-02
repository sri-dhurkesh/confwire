"""Generate versions.json for sphinx_material's version dropdown.

Run after `sphinx-multiversion` has built one subdirectory per ref under
the output directory (e.g. build/html/main/, build/html/v0.1.0/). Writes
build/html/versions.json mapping each ref name to its index page, which the
version_dropdown.js shipped with the sphinx_material theme fetches at
runtime.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: gen_versions_json.py <html-output-dir>")

    html_dir = Path(sys.argv[1])
    versions = {
        entry.name: f"{entry.name}/index.html"
        for entry in sorted(html_dir.iterdir())
        if entry.is_dir() and (entry / "index.html").exists()
    }
    if not versions:
        raise SystemExit(f"No built versions found under {html_dir}")

    (html_dir / "versions.json").write_text(json.dumps(versions, indent=2) + "\n")
    print(f"Wrote {html_dir / 'versions.json'} with versions: {', '.join(versions)}")


if __name__ == "__main__":
    main()
