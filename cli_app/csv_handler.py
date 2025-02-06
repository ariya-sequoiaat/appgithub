"""Module for writing GitHub repository details to CSV file.
It provides functions to append repository details to CSV file. 
If the file doesnt exist, it creates one with appropriate header. Each entry is timestamped. """
import csv
import os
import time
import logging
from datetime import datetime
from typing import Dict
from pathlib import Path

# Initialize logger at module level
logger = logging.getLogger('github_cli')

def write_to_csv(data: Dict[str, int], filename: str = 'output.csv') -> None:
    """
    Writes or appends data to a CSV file with a timestamp.
    If the username and repo_name differ from the previous entry, a new file will be created.
    data(dict): Dictionary containing repository details.
    filename (str, optional): The name of the csv file, default is 'output.csv'.
    Exception: If there is an error writing the file.
    """
    try:
        # Determine if the file exists using pathlib's exists method
        file_exists = Path(filename).exists()

        logger.debug(f"Checking if file exists: {filename} -> {file_exists}")

        if file_exists:
            # Read the file and check if it's empty
            with open(filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                rows = list(reader)  # Read all rows
                if rows:
                    last_row = rows[-1]  # Get the last row if the file is not empty
                    last_username = last_row[0] if last_row else None
                    last_repo_name = last_row[1] if last_row else None
                else:
                    last_username = None
                    last_repo_name = None
        else:
            last_username = None
            last_repo_name = None

        # Check if the current data matches the last row (username and repo_name)
        if last_username == data['username'] and last_repo_name == data['repo_name']:
            file_to_write = filename  # Use existing file
        else:
            # If different, create a new file with a new name
            file_to_write = f"{data['username']}_{data['repo_name']}_output.csv"
        
        logger.debug(f"Using file: {file_to_write}")

        # Open the appropriate file in append mode
        with open(file_to_write, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Write header only if the file is new (i.e., no data yet)
            if file.tell() == 0:  # file.tell() returns the current position in the file (0 means it's empty)
                writer.writerow(['Username', 'Repository', 'Branches', 'Stars', 'Forks', 'Timestamp'])

            # Append data with timestamp
            writer.writerow([
                data['username'],
                data['repo_name'],
                data['branches'],
                data['stars'],
                data['forks'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        logger.info(f"Data written to {file_to_write} successfully.")

    except Exception as e:
        logger.error(f"Error writing to CSV: {str(e)}")
        raise Exception(f"Error writing to CSV: {str(e)}")
