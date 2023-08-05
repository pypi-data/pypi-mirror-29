VIRTUALENV=.venv

.PHONY: build upload localdev test clean help travis

help:
	@echo "These are our make targets and what they do."
	@echo "All unlisted targets are internal."
	@echo ""
	@echo "  help:      Show this helptext"
	@echo "  localdev:  Setup local development env with a 'setup.py develop'"
	@echo "  build:     Create the distributions which we like to upload to pypi"
	@echo "  test:      Run the full suite of tests"
	@echo "  upload:    [build], but also upload to pypi using twine"
	@echo "  clean:     Remove typically unwanted files, mostly from [build]"


$(VIRTUALENV):
	virtualenv $(VIRTUALENV)
	$(VIRTUALENV)/bin/pip install --upgrade pip
	$(VIRTUALENV)/bin/pip install --upgrade setuptools


localdev: $(VIRTUALENV)
	$(VIRTUALENV)/bin/python setup.py develop


build: $(VIRTUALENV)
	$(VIRTUALENV)/bin/python setup.py sdist bdist_egg


$(VIRTUALENV)/bin/twine: $(VIRTUALENV) upload-requirements.txt
	$(VIRTUALENV)/bin/pip install -U -r upload-requirements.txt

upload: $(VIRTUALENV)/bin/twine build
	$(VIRTUALENV)/bin/twine upload dist/*


$(VIRTUALENV)/bin/flake8 $(VIRTUALENV)/bin/nose2: test-requirements.txt $(VIRTUALENV)
	$(VIRTUALENV)/bin/pip install -r test-requirements.txt
	touch $(VIRTUALENV)/bin/flake8
	touch $(VIRTUALENV)/bin/nose2

test: $(VIRTUALENV)/bin/flake8 $(VIRTUALENV)/bin/nose2 localdev
	$(VIRTUALENV)/bin/flake8
	$(VIRTUALENV)/bin/nose2 --verbose


travis:
	pip install --upgrade pip
	pip install --upgrade "setuptools>=29,<30"
	pip install -r test-requirements.txt
ifeq (, $(findstring pypy, $(TRAVIS_PYTHON_VERSION)))
	pip install "cryptography>=1.8.1,<2.0.0"
endif
	python setup.py develop
	flake8
	nose2 --verbose


clean:
	-rm -r $(VIRTUALENV)
	-rm -r dist
	-rm -r build
	-rm -r *.egg-info
