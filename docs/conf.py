"""Sphinx configuration for the confwire documentation."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

from confwire import __version__ as confwire_version

# -- Project information -----------------------------------------------------

project = "confwire"
copyright = "2026, confwire contributors"
author = "confwire contributors"
release = confwire_version
version = confwire_version

# Avoid Sphinx's default "confwire 0.1.0 documentation" title in the page
# <title> and header logo — keep the version visible only via the version
# dropdown instead.
html_title = "confwire"
html_short_title = "confwire"

# -- General configuration ----------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "myst_parser",
    "sphinx_tabs.tabs",
    "sphinx_multiversion",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

myst_enable_extensions = [
    "colon_fence",
    "deflist",
]

root_doc = "index"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# -- Options for sphinx-multiversion ------------------------------------------

# Build docs for the main branch and any semver-style release tag (v1.2.3).
smv_branch_whitelist = r"^main$"
smv_tag_whitelist = r"^v\d+\.\d+\.\d+$"
smv_remote_whitelist = r"^origin$"
smv_released_pattern = r"^refs/tags/v\d+\.\d+\.\d+$"
smv_outputdir_format = "{ref.name}"
smv_prefer_remote_refs = False

# -- Options for HTML output --------------------------------------------------

html_theme = "furo"
html_static_path = ["_static"]

# Brand logos live in the top-level assets/ directory and are copied into
# _static. Furo shows a separate variant in light and dark mode so the
# wordmark stays legible on both.
html_favicon = "_static/confwire_icon.svg"

html_theme_options = {
    "light_logo": "confwire_logo_color.svg",
    "dark_logo": "confwire_logo_darkmode.svg",
    "sidebar_hide_name": True,
    "source_repository": "https://github.com/sri-dhurkesh/confwire",
    "source_branch": "main",
    "source_directory": "docs/",
    "light_css_variables": {
        "color-brand-primary": "#4f46e5",
        "color-brand-content": "#4f46e5",
    },
    "dark_css_variables": {
        "color-brand-primary": "#a5b4fc",
        "color-brand-content": "#a5b4fc",
    },
}
