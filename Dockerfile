FROM python:3.11-slim

WORKDIR /app

# Install git and cleanup in single layer
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy only dependency files first
COPY pyproject.toml poetry.lock ./

# Install poetry and dependencies
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Copy application code
COPY cli_app/ ./cli_app/
COPY tests/ ./tests/

# Set default command
CMD ["python", "-m", "cli_app.main", "cli_app/input.json"]