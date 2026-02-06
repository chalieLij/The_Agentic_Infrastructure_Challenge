FROM python:3.9-slim

WORKDIR /app

# Install system dependencies if needed (none strictly for these python packages usually, maybe gcc for some deps)
# RUN apt-get update && apt-get install -y gcc

# Copy project definition
COPY pyproject.toml .
COPY src/ src/
COPY tests/ tests/

# Install dependencies including dev for testing
# We use 'pip install .[dev]' to install the project and dev deps defined in pyproject.toml
RUN pip install --no-cache-dir ".[dev]"

# Default command
CMD ["pytest"]
