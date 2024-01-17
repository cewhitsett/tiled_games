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

# Or use script
.PHONY: lint
lint:
		pylint tiled_tools --rcfile=.pylintrc
		pylint tests --rcfile=.pylintrc_test --ignore-paths="tests/snapshots"

.PHONY: format_fix
format_fix:
		isort --profile black tiled_tools tests scripts
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

# Run tests without formatting and not in verbose mode,
# useful for local development/unit testing
.PHONY: test_light
test_light:
		python -m unittest tests/test_*.py

# Make sure code is formatted before running tests,
# useful for CI/CD
.PHONY: test
test: format_fix
		python -m unittest -v tests/test_*.py

.PHONY: test_full
test_full:
		make lint
		make coverage

coverage:
		coverage run --source=tiled_tools -m unittest tests/test_*.py
		$(if $(format), coverage $(format), coverage report -m)

coverage_clean:
		coverage erase
		rm coverage_pretty.json

erase:
		coverage erase
		make clean

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
