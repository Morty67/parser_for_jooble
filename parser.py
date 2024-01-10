"""
Module: realty_parser

This module defines a Parser class for extracting real estate data,
from a list of links.
The parsed data includes information such as address, region, description,
pictures, price,number of bedrooms, and living area.

Classes:
- Parser: A class for parsing real estate data from a list of links.

Example Usage:
    from realty_parser import Parser
    from data_saver import DataSaver

    # List of real estate links to parse

    # Create an instance of the Parser class
    parser = Parser()

    # Parse real estate data from the provided links
    parser.parse_all_links(LIST_OF_ALL_LINKS)

    # Create an instance of the DataSaver class with parsed data
    data_saver = DataSaver(parser.data)

    # Save parsed data to a JSON file
    data_saver.save_data_to_json()
"""

import logging
from typing import List

import bs4
import requests

from data_saver import DataSaver
from get_all_links import LIST_OF_ALL_LINKS, HEADERS
from utils import (
    parse_photo_array,
    parse_price,
    parse_bedrooms,
    parse_living_area,
    parse_address,
    parse_description,
    parse_page_title, initialize_soup,
)


class Parser:

    """
    The Parser class is responsible for parsing real estate data,
        from a list of links.

    Attributes:
    - _base_headers (dict): Default headers for HTTP requests.
    - data (list): List to store the parsed real estate data.
    """

    def __init__(
        self, log_file: str = "parse_log.txt", log_level: int = logging.INFO
    ) -> None:
        """
        Constructor method to initialize the Parser instance.

        Parameters:
        - log_file (str): The name of the log file. Defaults to 'parse_log.txt'.
        - log_level (int): The logging level. Defaults to logging.INFO.
        """
        logging.basicConfig(filename=log_file, level=log_level)
        self.data = []

    def parse_link(self, link: str, soup: bs4.BeautifulSoup) -> None:
        """
        Parses real estate data from a given link and adds it to the data list.

        Parameters:
        - link (str): The link to the real estate property.
        - soup (bs4.BeautifulSoup): BeautifulSoup object containing, real
                estate information.
        """
        try:
            response = requests.get(link, headers=HEADERS)
            response.raise_for_status()
            count_bedrooms = parse_bedrooms(soup)
            living_area = parse_living_area(soup)
            photo_array = parse_photo_array(soup)
            price_text = parse_price(soup)
            address_info = parse_address(soup)
            description = parse_description(soup)
            page_title = parse_page_title(soup)
            self.data.append(
                {
                    "Link": link,
                    "PageTitle": page_title,
                    "Region": address_info[1],
                    "Address": address_info[0],
                    "Description": description,
                    "Pictures": photo_array,
                    "Price": price_text,
                    "Bedrooms": count_bedrooms,
                    "Area": living_area,
                }
            )
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch data for link {link}. Error: {e}")

    def parse_all_links(self, links: List[str]) -> None:
        """
        Parses real estate data from a list of links.

        Parameters:
        - links (list): List of links to real estate properties.
        """
        for link in links:
            try:
                response = requests.get(link, headers=HEADERS)
                response.raise_for_status()
                soup = initialize_soup(response.text)
                self.parse_link(link, soup)
            except requests.exceptions.RequestException as e:
                logging.error(
                    f"Failed to fetch data for link {link}. Error: {e}")


if __name__ == "__main__":
    parser = Parser()
    parser.parse_all_links(LIST_OF_ALL_LINKS)

    data_saver = DataSaver(parser.data)
    data_saver.save_data_to_json()
