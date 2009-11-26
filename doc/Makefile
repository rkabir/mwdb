# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
PAPER         = a4

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) rst

.PHONY: help clean html dirhtml pickle json htmlhelp qthelp latex changes linkcheck doctest

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  all	   to make html and text"
	@echo "  html      to make standalone HTML files"
	@echo "  text      to make txt files"
	@echo "  latex     to make LaTeX files, you can set PAPER=a4 or PAPER=letter"
	@echo "  clean     to clean all generated files"
	@echo "  changes   to make an overview of all changed/added/deprecated items"
	@echo "  linkcheck to check all external links for integrity"

clean:
	-rm -rf txt/*
	-rm -rf html/*
	-rm -rf doctrees/

all: html text

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) html
	@echo
	@echo "Build finished. The HTML pages are in ./html."

changes:
	$(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) changes
	@echo
	@echo "The overview file is in ./changes."

latex:
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) latex
	@echo
	@echo "Build finished; the LaTeX files are in build/latex."
	@echo "Run \`make all-pdf' or \`make all-ps' in that directory to" \
	      "run these through (pdf)latex."

linkcheck:
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in ./linkcheck/output.txt."

text:
	$(SPHINXBUILD) -b text $(ALLSPHINXOPTS) txt
	@echo
	@echo "Build finished. The txt files are in ./txt"
