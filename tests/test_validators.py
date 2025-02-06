import pytest
import sys
import os
from cli_app.validators import validate_username, validate_repo_name

# Test valid username
def test_validate_username_valid():
    assert validate_username('valid_user')

# Test invalid username
@pytest.mark.parametrize("username", ["", "invalid@user", "user#name"])
def test_validate_username_invalid(username):
    with pytest.raises(ValueError):
        validate_username(username)

# Test valid repository name
def test_validate_repo_name_valid():
    assert validate_repo_name('valid_repo')

# Test invalid repository name
@pytest.mark.parametrize("repo_name", ["", "repo!name", "repo name with space"])
def test_validate_repo_name_invalid(repo_name):
    with pytest.raises(ValueError):
        validate_repo_name(repo_name)
