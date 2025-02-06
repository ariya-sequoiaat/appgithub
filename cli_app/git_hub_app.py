import os
import time
import requests
import logging
from cli_app.validators import validate_username, validate_repo_name
from typing import Dict

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# GitHub API settings
BASE_URL = "https://api.github.com"

def get_github_token() -> str:
    """Safely retrieve GitHub token from environment"""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GitHub token is not set in environment variables")
    return token

def fetch_repo_details(username: str, repo_name: str) -> Dict[str, int]:
    """
    Fetches details like branches, stars, and forks from a GitHub repository.
    Implements retry logic, authentication, and validates inputs.
    """
    try:
        token = get_github_token()
    except ValueError as e:
        logging.error(str(e))
        return {}

    # Validate inputs
    validate_username(username)
    validate_repo_name(repo_name)

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    retries = 3
    backoff_factor = 2

    for attempt in range(retries):
        try:
            repo_url = f"{BASE_URL}/repos/{username}/{repo_name}"
            logging.debug(f"Fetching repo details from {repo_url}")

            response = requests.get(repo_url, headers=headers)
            logging.debug(f"Response status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()

                branches_url = f"{BASE_URL}/repos/{username}/{repo_name}/branches"
                branches_response = requests.get(branches_url, headers=headers)
                branches = len(branches_response.json()) if branches_response.status_code == 200 else 0

                return {
                    'username': username,
                    'repo_name': repo_name,
                    'branches': branches,
                    'stars': data.get('stargazers_count', 0),
                    'forks': data.get('forks_count', 0)
                }

            elif response.status_code == 401:
                logging.error("Invalid GitHub credentials (401 Unauthorized)")
                return {}
            elif response.status_code == 403:
                logging.warning("API rate limit exceeded (403). Waiting before retrying...")
                time.sleep(10)
            elif response.status_code == 404:
                logging.error(f"Repository not found: {username}/{repo_name}")
                return {}
            elif response.status_code in [500, 503]:
                logging.warning(f"GitHub API issue ({response.status_code})")
            else:
                logging.error(f"Unexpected error: {response.status_code}")
                return {}

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")

        if attempt < retries - 1:
            sleep_time = backoff_factor ** attempt
            logging.debug(f"Retrying in {sleep_time} seconds...")
            time.sleep(sleep_time)
        else:
            logging.error("Max retries reached")
            return {}