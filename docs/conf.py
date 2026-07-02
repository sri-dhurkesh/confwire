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

# sphinx-material injects a non-picklable function into html_context, which
# only affects the environment cache (not the build output) and cannot be
# avoided from user config.
suppress_warnings = ["config.cache"]

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

html_theme = "sphinx_material"
html_static_path = ["_static"]

html_theme_options = {
    "nav_title": "confwire",
    "color_primary": "indigo",
    "color_accent": "blue",
    "repo_url": "https://github.com/sri-dhurkesh/confwire",
    "repo_name": "confwire",
    "globaltoc_depth": 2,
    "globaltoc_collapse": True,
    "theme_color": "3f51b5",
}

html_sidebars = {
    "**": ["logo-text.html", "globaltoc.html", "versions.html", "searchbox.html"]
}
