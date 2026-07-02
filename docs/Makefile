# Minimal makefile for Sphinx documentation

SPHINXOPTS    ?=
SPHINXBUILD   ?= uv run sphinx-build
SPHINXMULTIVERSION ?= uv run sphinx-multiversion
SOURCEDIR     = .
BUILDDIR      = _build

.PHONY: help clean html multiversion

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean:
	rm -rf "$(BUILDDIR)"

html:
	$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

# Build one HTML site per whitelisted branch/tag (docs/conf.py: smv_*),
# each under $(BUILDDIR)/html/<ref-name>/, then generate the versions.json
# consumed by the sphinx_material version dropdown.
multiversion:
	$(SPHINXMULTIVERSION) "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)
	uv run python gen_versions_json.py "$(BUILDDIR)/html"

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
