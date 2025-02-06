import pytest
import os
import requests
from unittest.mock import patch, MagicMock
from cli_app.git_hub_app import fetch_repo_details, get_github_token

def mock_github_response(status_code, json_data=None):
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_response.json.return_value = json_data if json_data else {}
    return mock_response

@pytest.fixture
def mock_env_token():
    """Fixture to set up test environment token"""
    original_token = os.environ.get('GITHUB_TOKEN')
    os.environ['GITHUB_TOKEN'] = 'test_token'
    yield
    if original_token:
        os.environ['GITHUB_TOKEN'] = original_token
    else:
        del os.environ['GITHUB_TOKEN']

def test_get_github_token_missing():
    """Test get_github_token when token is not set"""
    if 'GITHUB_TOKEN' in os.environ:
        del os.environ['GITHUB_TOKEN']
    with pytest.raises(ValueError):
        get_github_token()

def test_get_github_token_success(mock_env_token):
    """Test get_github_token with valid token"""
    assert get_github_token() == 'test_token'

@patch('cli_app.git_hub_app.requests.get')
def test_fetch_repo_details_success(mock_get, mock_env_token):
    """Test fetch_repo_details with successful response"""
    mock_get.return_value = mock_github_response(200, {
        "stargazers_count": 15,
        "forks_count": 5
    })
    result = fetch_repo_details("testuser", "TestRepo")
    
    assert result != {}
    assert result['username'] == "testuser"
    assert result['repo_name'] == "TestRepo"
    assert result['stars'] == 15
    assert result['forks'] == 5

@patch('cli_app.git_hub_app.requests.get')
def test_fetch_repo_details_not_found(mock_get, mock_env_token):
    """Test fetch_repo_details with 404 response"""
    mock_get.return_value = mock_github_response(404)
    result = fetch_repo_details("testuser", "NonExistentRepo")
    assert result == {}

@patch('cli_app.git_hub_app.requests.get')
def test_fetch_repo_details_unauthorized(mock_get, mock_env_token):
    """Test fetch_repo_details with 401 response"""
    mock_get.return_value = mock_github_response(401)
    result = fetch_repo_details("testuser", "TestRepo")
    assert result == {}

@patch('cli_app.git_hub_app.requests.get')
def test_fetch_repo_details_server_error(mock_get, mock_env_token):
    """Test fetch_repo_details with 500 response"""
    mock_get.return_value = mock_github_response(500)
    result = fetch_repo_details("testuser", "TestRepo")
    assert result == {}