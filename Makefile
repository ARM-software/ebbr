# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = EBBR
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo
	@echo 'Use "make text html singlehtml latexpdf" to generate the EBBR'
	@echo 'specification in the main supported formats.'
	@echo
	@echo 'Use "make check" to perform verifications on this repository.'

.PHONY: help Makefile check check-local

check-local:
	! grep -r --file=.typos.txt --exclude=.typos.txt --exclude-dir=.git
	yamllint .
	flake8 .
	mypy .

check: check-local linkcheck

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
