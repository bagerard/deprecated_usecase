MAKEFLAGS += --silent

.PHONY: setup-venv

PYTHON_VERSION = "3.6.5"
VENV_NAME := $(shell cat .python-version)

setup-venv: _install_python_version _install_virtualenv _install_usecase


_install_python_version:
	# Ensures that the version of python required by CMP is installed
	echo "-- Checking python pyenv $ installation..."
	if pyenv versions | grep -q $(PYTHON_VERSION); then \
		echo "- python $(PYTHON_VERSION) installation was found in pyenv"; \
	else \
		echo "- python $(PYTHON_VERSION) installation was not found in pyenv, installing it..."; \
		pyenv install $(PYTHON_VERSION); \
	fi

_install_virtualenv:
	# Resets the CMP virtual env
	echo "-- Installing virtual env..."
	echo "- Uninstalling previous venv..."
	pyenv uninstall -f $(VENV_NAME)
	echo "- Installing venv..."
	pyenv virtualenv $(PYTHON_VERSION) $(VENV_NAME)
	echo "- Upgrading pip..."
	pip install --upgrade pip


_install_usecase:
	echo "Installing cmp packages and dependencies..."
	pip install -e ../py-usecase
