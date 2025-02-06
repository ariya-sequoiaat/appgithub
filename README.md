# CLI Repository Details Fetcher

This is a command-line interface (CLI) based application that allows you to fetch various details about a GitHub repository such as:

- Number of commits
- Number of stars
- Number of branches
- Number of forks

The results are saved in CSV format. You will need to provide the GitHub username and repository name in a `.json` format as input. To avoid hitting GitHub's API rate limits, you need to provide your GitHub Personal Access Token (PAT).


## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Docker Setup](#docker-setup)
- [Make Commands](#make-commands)


## Requirements

- Python 3.x
- Docker (Optional, for containerized setup)
- GitHub Personal Access Token (PAT)


## Installation

1. Clone the repository:
   git clone https://github.com/yourusername/cli-repository-details-fetcher.git
   cd cli-repository-details-fetcher

Install dependencies:
If you're using Python, create a virtual environment and install the dependencies:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Export your GitHub Personal Access Token (PAT): 
Before running the application, you must export your GitHub PAT. This ensures the app can access GitHub's API without hitting rate limits.
This is how it can be done.
export GITHUB_TOKEN=your_git_hub_personal_access_token

Usage
Input Format
You need to provide a input.json file with the following structure:
{
  "username": "your-github-username",
  "repository": "your-repository-name"
}

Running the Application
Once you've exported your GitHub token, you can run the program as follows:

python cli_app/main.py input.json

This will output a CSV file with the requested repository details (commits, stars, branches, forks).

Running the Application in Docker

Install Docker if not already installed:
sudo apt update -y
sudo apt install docker.io -y
Build the Docker image:
docker build -t aryaapp:latest .

Run the Docker container:
docker run --rm -e GITHUB_TOKEN=your_git_hub_PAT_personal_access_token aryaapp:latest

Docker Compose Setup
To use Docker Compose for setting up the environment, you can follow these steps:

Build the Docker Compose environment:
docker-compose build

Run the application using Docker Compose:
docker-compose run --rm aryaapp

Make Commands
If you prefer to use Make commands for managing the project, here are some available options:

Build Docker Image:
make docker-build

Run Docker Container:
make docker-run

Build and Run the Application:
make build
make run

Run Tests:
To run tests using pytest:
make test

Clean the Build:
make clean


File Structure

cli-app

├── Dockerfile                  # Docker setup file

├── Makefile                    # Make commands for building and running

├── README.md                   # Project documentation

├── cli_app                     # Core application files

│   ├── __init__.py

│   ├── csv_handler.py          # Handles CSV file operations

│   ├── git_hub_app.py          # Contains logic for interacting with GitHub API

│   ├── input.json              # Example input file (GitHub username & repository)

│   ├── logger.py               # Logging utility

│   ├── main.py                 # Main entry point of the application

│   └── validators.py           # Validation logic for inputs

├── docker-compose.yml          # Docker Compose file

├── pyproject.toml              # Python project setup file

└── tests                       # Unit tests

    ├── __init__.py

    ├── test_csv_handler.py     # Unit tests for CSV handler

    ├── test_git_hub_app.py     # Unit tests for GitHub API interaction

    ├── test_logger.py          # Unit tests for logger

    ├── test_main.py            # Unit tests for main app functionality

    └── test_validators.py      # Unit tests for validators
    

Conclusion
This CLI app allows you to fetch useful repository details from GitHub and save them in a CSV format. By using Docker or Makefile, you can easily set up and run the application in a containerized environment or locally. Don't forget to set your GitHub PAT to avoid rate limits when accessing GitHub's API.