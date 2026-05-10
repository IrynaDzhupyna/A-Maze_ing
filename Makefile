SRC = .
NAME = a_maze_ing.py
CONFIG = config.txt

VENV = .venv

run: install
	uv run $(NAME) $(CONFIG)

install: $(VENV)

# create a virtual enviroment in inside existing folder
$(VENV): pyproject.toml
	pip install uv
	uv venv --python 3.10.12
	uv sync --all-groups

debug:
	uv run python -m pdb $(NAME) $(CONFIG)

clean:
	rm -rf $(VENV) */__pycache__ .mypy_cache .pytest_cache

lint:
	uvx flake8 $(SRC)
	uv run mypy $(SRC) --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uvx flake8 $(SRC)
	uv run mypy --strict $(SRC)

test:
	uvx --with pytest pytest 

.PHONY: run install debug clean lint lint-strict test