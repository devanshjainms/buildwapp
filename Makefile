PYTHON?=python3
VENV=.venv

setup:
$(PYTHON) -m venv $(VENV)
$(VENV)/bin/pip install --upgrade pip
$(VENV)/bin/pip install -r requirements.txt

run:
$(VENV)/bin/flask --app app run

dev:
FLASK_ENV=development $(MAKE) run

test:
$(VENV)/bin/pytest

