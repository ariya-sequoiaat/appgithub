import re

def validate_username(username: str) -> bool:
    """
    Validates GitHub username format.
    """
    if not isinstance(username, str) or not username:
        raise ValueError("Invalid GitHub username: username cannot be empty")
    # Updated regex to allow underscores and more flexible usernames
    if not re.match(r'^[a-zA-Z0-9][-a-zA-Z0-9_]{0,38}[a-zA-Z0-9]$', username):
        raise ValueError("Invalid GitHub username format")
    return True

def validate_repo_name(repo_name: str) -> bool:
    """
    Validates GitHub repository name format.
    """
    if not isinstance(repo_name, str) or not repo_name:
        raise ValueError("Invalid GitHub repository name: name cannot be empty")
    if not re.match(r'^[a-zA-Z0-9_.-]+$', repo_name):
        raise ValueError("Invalid GitHub repository name format")
    return True

