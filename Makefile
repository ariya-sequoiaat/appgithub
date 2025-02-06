.PHONY: build run test clean docker-build docker-run docker-clean all help

# Variables
DOCKER_IMAGE = aryaapp
DOCKER_TAG = latest
DOCKER_CONTAINER = aryaapp_container
PYTHON_MODULE = cli_app.main
INPUT_FILE = cli_app/input.json

# Python commands
build:
	poetry install

run:
	@if [ -z "$$GITHUB_TOKEN" ]; then \
		echo "Error: GITHUB_TOKEN environment variable is not set"; \
		exit 1; \
	fi
	poetry run python -m $(PYTHON_MODULE) $(INPUT_FILE)

test:
	poetry run pytest -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf dist build

# Docker commands
docker-build:
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

docker-run:
	@if [ -z "$$GITHUB_TOKEN" ]; then \
		echo "Error: GITHUB_TOKEN environment variable is not set"; \
		exit 1; \
	fi
	docker run --rm -e GITHUB_TOKEN=$$GITHUB_TOKEN $(DOCKER_IMAGE):$(DOCKER_TAG)

docker-clean:
	-docker stop $(DOCKER_CONTAINER) 2>/dev/null || true
	-docker rm $(DOCKER_CONTAINER) 2>/dev/null || true
	-docker rmi $(DOCKER_IMAGE):$(DOCKER_TAG) 2>/dev/null || true

# Combined commands
all: clean build test docker-build

help:
	@echo "Usage:"
	@echo "  make [command]"
	@echo ""
	@echo "Commands:"
	@echo "  build         Install project dependencies"
	@echo "  run          Run the CLI application"
	@echo "  test         Run tests with verbose output"
	@echo "  clean        Clean up Python cache and build files"
	@echo "  docker-build Build Docker image"
	@echo "  docker-run   Run Docker container"
	@echo "  docker-clean Clean up Docker resources"
	@echo "  all          Run clean, build, test, and docker-build"
	@echo ""
	@echo "Environment:"
	@echo "  GITHUB_TOKEN must be set for run and docker-run commands. The format is export GITHUB_TOKEN=your_git_hub_token_PAT "