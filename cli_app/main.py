"""Module for executing the main CLI functionality for fetching GitHub repository details and save them to the csv file.
It reads .json file, fetches details from gitHub repository and writes them to the csv file. 
It also handles errors in file reading, json parsing and other exceptions"""

import json
import sys
from pathlib import Path
from cli_app.git_hub_app import fetch_repo_details
from cli_app.csv_handler import write_to_csv
from cli_app.logger import setup_logger

def main(input_file: str) -> None:
    """
    Main function that reads input.json, fetches GitHub details, and writes to CSV.
    Additionally it handles exceptions such as file not found, invalid json format, missing keys in JSON, and other exceptions.
    """
    logger = setup_logger()

    try:
        # Read input JSON file
        with open(input_file, 'r') as file:
            data = json.load(file)
        
        username = data.get('username')
        repo_name = data.get('repository_name')
        
        if not username or not repo_name:
            raise ValueError("Invalid input file. Ensure 'username' and 'repository_name' are present.")
        
        # Fetch GitHub details
        try:
            repo_details = fetch_repo_details(username, repo_name)
        except Exception as e:
            logger.error(f"Error: Failed to fetch repository details from GitHub - {str(e)}")
            sys.exit(5)  # Exit code for GitHub fetch failure
        
        # Write to CSV
        try:
            write_to_csv(repo_details)
            logger.info(f"Details for {repo_name} by {username} written to CSV.")
        except Exception as e:
            logger.error(f"Error: Failed to write to CSV - {str(e)}")
            sys.exit(6)  # Exit code for CSV writing failure
        
    except FileNotFoundError:
        logger.error(f"Error: Input file '{input_file}' not found")
        sys.exit(2)  # Exit code for file not found error
    except json.JSONDecodeError as e:
        logger.error(f"Error: Invalid JSON format in input file - {str(e)}")
        sys.exit(3)  # Exit code for invalid JSON format
    except ValueError as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(4)  # Exit code for missing keys in JSON (username/repository_name)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)  # Exit code for general errors

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python -m cli_app.main <input.json>")
        sys.exit(1)  # Exit code for invalid command line usage
    
    main(sys.argv[1])
