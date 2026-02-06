.PHONY: setup test lint clean

# Install dependencies from pyproject.toml (including dev dependencies)
setup:
	pip install -e ".[dev]"

# Run pytest inside a Docker container
test:
	docker build -t chimera-test .
	docker run --rm chimera-test pytest -v

# Run ruff for linting
lint:
	ruff check .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
