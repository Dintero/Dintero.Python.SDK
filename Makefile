VENV_NAME?=venv
PYTHON?=python3

venv: $(VENV_NAME)/bin/activate

$(VENV_NAME)/bin/activate: setup.py
	@test -d $(VENV_NAME) || $(PYTHON) -m venv $(VENV_NAME)
	${VENV_NAME}/bin/python -m pip install -U pip tox
	${VENV_NAME}/bin/python -m pip install -e .
	${VENV_NAME}/bin/python -m pip install -e '.[dev]'
	@touch $(VENV_NAME)/bin/activate

test: venv
	@${VENV_NAME}/bin/tox -p auto $(TOX_ARGS)

fmt: venv
	@${VENV_NAME}/bin/tox -e fmt

fmtcheck: venv
	@${VENV_NAME}/bin/tox -e fmt -- --check --verbose

lint: venv
	@${VENV_NAME}/bin/tox -e lint

clean:
	@rm -rf .coverage .coverage.* build/ dist/ htmlcov/

.PHONY: venv test fmt fmtcheck lint clean
