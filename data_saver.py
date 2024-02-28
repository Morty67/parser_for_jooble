"""
Module: data_saver

This module defines a DataSaver class for saving parsed data to a JSON file.

Classes:
- DataSaver: A class for saving parsed data to a JSON file.

Example Usage:
    from data_saver import DataSaver

    # Parsed real estate data to be saved
    parsed_data = [...]

    # Create an instance of the DataSaver class
    data_saver = DataSaver(parsed_data)

    # Save parsed data to a JSON file
    data_saver.save_data_to_json()
"""

import json
import logging
from typing import List, Dict, Any


class DataSaver:

    """
    A class for saving parsed data to a JSON file.

    Attributes:
        data (List[Dict[str, Any]]): Parsed data to be saved.
        log_file (str): The log file to record information,
            about the saving process.
    """

    def __init__(
        self, data: List[Dict[str, Any]], log_file: str = "parse_log.txt"
    ):
        """
        Initialize the DataSaver instance.

        Parameters:
            data (List[Dict[str, Any]]): Parsed data to be saved.
            log_file (str): The log file to record information about,
                the saving process.
        """
        self.data = data
        self.log_file = log_file

    def save_data_to_json(self, output_file: str = "output.json") -> None:
        """
        Save the data to a JSON file.

        Parameters:
            output_file (str): The output file to save the data to.
        Raises:
            Exception: If there is an error during the saving process.
        """
        try:
            with open(output_file, "w") as json_file:
                json.dump(self.data, json_file, indent=2)
            logging.info("Data extraction completed.")
        except Exception as e:
            logging.error(f"Failed to save data to {output_file}. Error: {e}")
