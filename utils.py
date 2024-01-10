"""
Module: utils

This module provides utility functions for parsing real estate data,
from HTML text.

Functions:
- parse_address(html_text: str) -> tuple[str, str | None]: Parses the
address, and region from HTML text.
- parse_photo_array(html_text: str) -> Union[str, List[str]]: Parses the
array, of photo URLs from HTML text.
- parse_price(html_text: str) -> Union[str, float]: Parses the price,
from HTML text.
- parse_bedrooms(html_text: str) -> Union[str, int]: Parses the number,
of bedrooms from HTML text.
- parse_living_area(html_text: str) -> str: Parses the living area,
from HTML text.
- parse_description(html_text: str) -> str: Parses the description,
from HTML text.
- parse_page_title(html_text: str) -> Optional[str]: Parses the page title,
from HTML text.

Example Usage:
    from utils import parse_address, parse_price

    # HTML text containing real estate information
    html_text = "<html>...</html>"

    # Parse address and region
    address, region = parse_address(html_text)

    # Parse price
    price = parse_price(html_text)
"""

import json
from typing import Union, List, Optional

import bs4


def parse_address(html_text: str) -> tuple[str, str | None]:
    """
    Parse the address and region from HTML text.

    Args:
        html_text (str): HTML text containing real estate information.

    Returns:
        tuple[str, str | None]: A tuple containing the address and region,
            (if available).
    """
    soup = bs4.BeautifulSoup(html_text, "html.parser")
    address_element = soup.find(
        "h2", {"itemprop": "address", "class": "pt-1"}
    )
    if address_element:
        address_text = address_element.text.strip()
        address_parts = address_text.split(", ", 1)
        if len(address_parts) == 2:
            address = address_text
            region = address_parts[1]
        else:
            address, region = address_text, None
        return address, region


def parse_photo_array(html_text: str) -> Union[str, List[str]]:
    """
    Parse the array of photo URLs from HTML text.

    Args:
        html_text (str): HTML text containing real estate information.

    Returns:
        Union[str, List[str]]: A list of photo URLs or an error message,
            if the script tag is not found.
    """
    soup = bs4.BeautifulSoup(html_text, "html.parser")
    script_tag = soup.find(
        "script", string=lambda s: "window.MosaicPhotoUrls" in s
    )
    if script_tag:
        script_text = script_tag.text
        # Select a row that contains an array of photos
        start_index = script_text.find("[")
        end_index = script_text.find("]") + 1
        photo_array_str = script_text[start_index:end_index]
        photo_array = json.loads(photo_array_str)

        return photo_array
    else:
        return "Script tag not found."


def parse_price(html_text: str) -> Union[str, float]:
    """
    Parse the price from HTML text.

    Args:
        html_text (str): HTML text containing real estate information.

    Returns:
        Union[str, float]: The price as a string or float, or an error
            message, if the price element is not found.
    """
    soup = bs4.BeautifulSoup(html_text, "html.parser")

    price_element = soup.find("span", {"class": "text-nowrap"})

    if price_element:
        price_text = price_element.parent.text.split()
        price_text = price_text[1] + price_text[2]

        return price_text
    else:
        return "Price element not found."


def parse_bedrooms(html_text: str) -> Union[str, int]:
    """
    Parse the number of bedrooms from HTML text.

    Args:
        html_text (str): HTML text containing real estate information.

    Returns:
        Union[str, int]: The number of bedrooms as a string or integer,
            or an error message if the element is not found.
    """
    soup = bs4.BeautifulSoup(html_text, "html.parser")
    bedrooms_element = soup.find("div", {"class": "cac"})

    if bedrooms_element:
        bedrooms_text = bedrooms_element.text.strip()
        return bedrooms_text
    else:
        return "Bedrooms element not found."


def parse_living_area(html_text: str) -> str:
    """
    Parse the living area from HTML text.

    Args:
        html_text (str): HTML text containing real estate information.

    Returns:
        str: The living area as a string, or an error message, if the
            element is not found.
    """
    soup = bs4.BeautifulSoup(html_text, "html.parser")

    living_area_element = soup.find("div", {"class": "carac-value"})

    if living_area_element:
        living_area_text = living_area_element.find("span").text.strip()

        return living_area_text
    else:
        return "Living area element not found."


def parse_description(html_text: str) -> str:
    """
    Parse the description from HTML text.

    Args:
        html_text (str): HTML text containing real estate information.

    Returns:
        str: The description as a string, or an error message, if the
            element is not found.
    """
    soup = bs4.BeautifulSoup(html_text, "html.parser")
    description_element = soup.find("div", {"itemprop": "description"})
    if description_element:
        description_text = description_element.text.strip()
        return description_text
    else:
        return "No description available."


def parse_page_title(html_text: str) -> Optional[str]:
    """
    Parse the page title from HTML text.

    Args:
        html_text (str): HTML text containing real estate information.

    Returns:
        Optional[str]: The page title as a string, or None if, the element
            is not found.
    """
    soup = bs4.BeautifulSoup(html_text, "html.parser")
    page_title = soup.find("span", {"data-id": "PageTitle"})
    if page_title:
        page_title_text = page_title.text.strip()
        return page_title_text
    else:
        return None
