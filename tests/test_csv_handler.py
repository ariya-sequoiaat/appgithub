import pytest
import os
import csv
import logging
from datetime import datetime
from pathlib import Path
from cli_app.csv_handler import write_to_csv
from cli_app.logger import setup_logger

@pytest.fixture(autouse=True)
def setup_logging():
    """Fixture to set up logging before each test"""
    logger = setup_logger()
    return logger

@pytest.fixture
def valid_repo_data():
    """
    Fixture that returns valid repository data to be written to the CSV file.
    """
    return {
        'username': 'test-user',
        'repo_name': 'test_repo',
        'branches': 5,
        'stars': 10,
        'forks': 3
    }

