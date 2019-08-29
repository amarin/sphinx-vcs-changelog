# Minimal makefile for Sphinx documentation

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXAPIDOC  = sphinx-apidoc
SOURCEDIR     = ./docs
BUILDDIR      = ./.build
PAPER		  = a4
DOCTARGET	  = ~

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile \
developdoc documentation commit_changelog \
install_docs_setup_cfg rm_docs_setup_cfg \
patch_docs_cfg patch_docs patch_bumpversion patch_version \
minor_docs_cfg minor_docs minor_bumpversion minor_version \
major_docs_cfg major_docs major_bumpversion major_version \
push release


# Macros to have VERSION from setup.cfg
GREP_VERSION = $(shell cat docs/docs.cfg | grep "version" | awk '{printf $$3}')
TAKE_VERSION = $(eval VERSION=$(GREP_VERSION))

# Macros to have PACKAGE from setup.cfg
GREP_PACKAGE = $(shell cat docs/docs.cfg | grep "package" | awk '{printf $$3}')
TAKE_PACKAGE = $(eval PACKAGE=$(GREP_PACKAGE))

## Catch-all target: route all unknown targets to Sphinx using the new
## "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
#%: Makefile
#	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).

tests:
	rm -rf $(BUILDDIR)/cov
	$(BINDIR)/pytest && rm pytest.logs && rm debug.log

developdoc:
	pip3.6 install -r docs/requirements.txt

documentation:

	$(TAKE_VERSION)
	$(TAKE_PACKAGE)
	@echo "Build $(PACKAGE)-$(VERSION) documentation"
	python3.6 setup.py build_sphinx

	@echo "Copy CHANGELOG & README to root"
	cp $(BUILDDIR)/text/changelog.txt ./CHANGELOG.txt
	cp $(BUILDDIR)/text/about.txt ./README.txt

	@echo "Running LaTeX files through pdflatex..."
	$(MAKE) LATEXMKOPTS="-silent" -C $(BUILDDIR)/latex all-pdf

	@echo "Copy PDF & html.zip to ~"

	cd $(BUILDDIR); \
	zip -r $(PACKAGE)-$(VERSION)-html.zip html;\
	mv $(PACKAGE)-$(VERSION)-html.zip $(DOCTARGET)/ ;\
	mv latex/$(PACKAGE).pdf $(DOCTARGET)/$(PACKAGE)-$(VERSION).pdf ;\
	cd ..

commit_changelog:
	git add CHANGELOG.txt
	git commit -m ":build: Обновлён список изменений версии"

preserve_docs_cfg:
	cp docs/docs.cfg docs/.docs.save
	cp docs/docs.cfg ./setup.cfg

restore_docs_cfg:
	mv -f docs/.docs.save docs/docs.cfg
	rm setup.cfg

preserve_bumpversion_docs:
	cp .bumpversion.docs.cfg .bumpversion.docs.save

restore_bumpversion_docs:
	mv -f .bumpversion.docs.save .bumpversion.docs.cfg

patch_docs_cfg:
	bumpversion --allow-dirty --config-file .bumpversion.docs.cfg patch

minor_docs_cfg:
	bumpversion --allow-dirty --config-file .bumpversion.docs.cfg minor

major_docs_cfg:
	bumpversion --allow-dirty --config-file .bumpversion.docs.cfg major

patch_bumpversion:
	bumpversion patch

minor_bumpversion:
	bumpversion minor

major_bumpversion:
	bumpversion major

patch_docs:	preserve_bumpversion_docs preserve_docs_cfg \
patch_docs_cfg documentation restore_bumpversion_docs restore_docs_cfg

minor_docs: preserve_bumpversion_docs preserve_docs_cfg \
minor_docs_cfg documentation restore_bumpversion_docs restore_docs_cfg

major_docs: preserve_bumpversion_docs preserve_docs_cfg \
major_docs_cfg documentation restore_bumpversion_docs restore_docs_cfg

patch_version: patch_docs commit_changelog patch_bumpversion
minor_version: minor_docs commit_changelog minor_bumpversion
major_version: major_docs commit_changelog minor_bumpversion

push:
	git push origin master --tags

docs: preserve_docs_cfg documentation restore_docs_cfg
release : patch_version push
