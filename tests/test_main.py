import pytest
from unittest.mock import patch, mock_open
from cli_app.main import main

@patch('cli_app.main.open', new_callable=mock_open, read_data='{"username": "test_user", "repository_name": "test_repo"}')
@patch('cli_app.main.fetch_repo_details')
@patch('cli_app.main.write_to_csv')
@patch('cli_app.main.setup_logger')
def test_main_valid_input(mock_logger, mock_write_to_csv, mock_fetch_repo_details, mock_file):
    mock_fetch_repo_details.return_value = {
        'username': 'test_user',
        'repo_name': 'test_repo',
        'branches': 5,
        'stars': 10,
        'forks': 3
    }
    
    mock_logger.return_value = mock_logger
    
    main('test_input.json')
    mock_write_to_csv.assert_called_once_with(mock_fetch_repo_details.return_value)

@patch('cli_app.main.open')
@patch('cli_app.main.setup_logger')
def test_main_file_not_found(mock_logger, mock_file):
    mock_logger.return_value = mock_logger
    mock_file.side_effect = FileNotFoundError()
    
    with pytest.raises(SystemExit) as excinfo:
        main('non_existent_file.json')
    assert excinfo.value.code == 2


