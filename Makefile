NAME = a_maze_ing.py
PYTHON = python3
PIP = pipx
VENV = .venv


run: install
	$(PYTHON) $(NAME)

install:
	$(PIP) install -r requirements.txt

debug: 
	$(PYTHON) -m pdb $(NAME)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .mypy_cache
	rm -rf build dist *.egg-info

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

reformat:


test:

update:



.PHONY: run install debug clean lint lint-strict reformat test update
