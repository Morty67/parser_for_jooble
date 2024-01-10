"""
Module: parser

This module defines an AsyncParser class for asynchronously extracting,
real estate data,
from a list of links. The parsed data includes information such as address,
region, description, pictures, price, number of bedrooms, and living area.

Classes:
- AsyncParser: An asynchronous class for parsing real estate data from,
a list of links.

Example Usage:
    from realty_parser import AsyncParser
    from data_saver import DataSaver

    # List of real estate links to parse

    # Create an instance of the AsyncParser class
    async_parser = AsyncParser()

    # Parse real estate data asynchronously from the provided links
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        async_parser.parse_all_links_async(LIST_OF_ALL_LINKS)
    )
    # Create an instance of the DataSaver class with asynchronously parsed data
    data_saver = DataSaver(async_parser.data)

    # Save parsed data to a JSON file
    data_saver.save_data_to_json()
"""

import asyncio
import logging
from typing import List

import aiohttp
import bs4

from data_saver import DataSaver
from get_all_links import LIST_OF_ALL_LINKS, HEADERS
from utils import (
    parse_photo_array,
    parse_price,
    parse_bedrooms,
    parse_living_area,
    parse_address,
    parse_description,
    parse_page_title,
    initialize_soup,
)


class AsyncParser:

    """
    Asynchronous web scraper for real estate data.

    This class is designed to asynchronously fetch and parse real estate data
    from a list of links. It uses aiohttp for asynchronous HTTP requests and
    BeautifulSoup for HTML parsing.

    Attributes:
    - log_file (str): The name of the log file for logging.
    - log_level (int): The logging level. Defaults to logging.INFO.
    - data (list): List to store the parsed real estate data.
    """

    def __init__(
        self, log_file: str = "parse_log.txt", log_level: int = logging.INFO
    ) -> None:
        """
        Initialize the AsyncParser instance.

        Parameters:
        - log_file (str): The name of the log file. Defaults,
            to 'parse_log.txt'.
        - log_level (int): The logging level. Defaults to logging.INFO.
        """
        logging.basicConfig(filename=log_file, level=log_level)
        self.data = []

    async def fetch_data(self, session, link):
        """
        Asynchronously fetch data from a given link using aiohttp session.

        Parameters:
        - session: aiohttp.ClientSession: The aiohttp session object.
        - link (str): The link to fetch data from.
        """
        try:
            async with session.get(link, headers=HEADERS) as response:
                response.raise_for_status()
                html = await response.text()
                soup = initialize_soup(html)
                self.parse_link(link, soup)
        except aiohttp.ClientError as e:
            logging.error(f"Failed to fetch data for link {link}. Error: {e}")

    async def parse_all_links_async(self, links: List[str]):
        """
        Asynchronously parse real estate data from a list of links.

        Parameters:
        - links (List[str]): List of links to real estate properties.
        """
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_data(session, link) for link in links]
            await asyncio.gather(*tasks)

    def parse_link(self, link: str, soup: bs4.BeautifulSoup) -> None:
        """
        Parse real estate data from a given link and add it to the data list.

        Parameters:
        - link (str): The link to the real estate property.
        - soup (bs4.BeautifulSoup): BeautifulSoup object containing real,
            estate information.
        """
        try:
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
        except Exception as e:
            logging.error(f"Failed to parse data for link {link}. Error: {e}")


if __name__ == "__main__":
    import time

    start_time = time.time()

    async_parser = AsyncParser()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        async_parser.parse_all_links_async(LIST_OF_ALL_LINKS)
    )

    data_saver = DataSaver(async_parser.data)
    data_saver.save_data_to_json()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time} seconds")
