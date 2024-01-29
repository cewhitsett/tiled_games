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
		black --check tiled_tools games tests backend

# Or use script.
# Most type checkers do not do well with "Number", a critical
# type for the tiled_tools package. This is moreso to do with the fact that
# Number is a fairly complex type. So, just use it for game classes now
.PHONY: lint
lint:
		pylint tiled_tools games --rcfile=.pylintrc
		pylint tests --rcfile=.pylintrc_test --ignore-paths="tests/snapshots"
		pytype games/twenty_forty_eight/game.py

.PHONY: format_fix
format_fix:
		isort --profile black tiled_tools tests scripts games
		black tiled_tools tests scripts games backend

# Builds initial RST files for doc site, does not overwrite existing files
apidoc:
		sphinx-apidoc -o docs/source/ tiled_tools games

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
		make format
		make coverage

coverage:
		coverage run --source=tiled_tools,games -m unittest tests/test_*.py
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
