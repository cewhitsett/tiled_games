SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docs/source
BUILDDIR      = docs/build

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile


# https://www.freecodecamp.org/news/auto-format-your-python-code-with-black/,
# has a tutorial on how to set up black for jupyter notebook, may be interesting
# to look into
.PHONY: format
format:
		black --check tiled_tools tests

.PHONY: format_fix
format_fix:
		black tiled_tools tests

# Builds initial RST files for doc site, does not overwrite existing files
apidoc:
		sphinx-apidoc -o docs/source/ tiled_tools

.PHONY: requirements
requirements:
		pip freeze > requirements.txt

.PHONY: install_requirements
install_requirements:
		pip install -r requirements.txt

.PHONY: snapshots
snapshots:
		nosetests --snapshot-update
		make format_fix

# Make sure code is formatted before running tests,
# useful for CI/CD
.PHONY: test
test: format
		python -m unittest -v tests/test_*.py

# Run tests without formatting and not in verbose mode,
# useful for local development/unit testing
.PHONY: test_light
test_light:
		python -m unittest tests/test_*.py

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
