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
		black --check tiled_tools tests --exclude 'test/snapshots/*.py'

.PHONY: format_fix
format_fix:
		black tiled_tools tests --exclude 'test/snapshots/*.py'

# Builds initial RST files for doc site, does not overwrite existing files
apidoc:
		sphinx-apidoc -o docs/source/ tiled_tools

.PHONY: requirements
requirements:
		pip freeze > requirements.txt

.PHONY: install_requirements
install_requirements:
		pip install -r requirements.txt

.PHONY: test
test: format
		python -m unittest -v tests/test_*.py

# Does not run format before running tests and does not run
# tests in verbose mode
.PHONY: test_light
test_light:
		python -m unittest tests/test_*.py

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
