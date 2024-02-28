"""
Module: get_all_links

This module provides functions to scrape real estate links
from the "https://realtylink.org/en/properties~for-rent?uc=0" website.

Functions:
- get_all_links_from_page(url: str) -> List[str]: Retrieves all property
links, from a given page.
- scrape_links_with_selenium(url: str, num_pages: int = 3) -> None:
Uses Selenium to scrape property links from multiple pages.

Global Variables:
- URL (str): The base URL of the real estate website.
- LIST_OF_ALL_LINKS (List[str]): A list to store all scraped property links.

Example Usage:
    from realty_scraper import scrape_links_with_selenium, LIST_OF_ALL_LINKS

    # Scrape property links using Selenium
    scrape_links_with_selenium(URL)

    # Access the list of all scraped property links
    print(LIST_OF_ALL_LINKS)
"""
from typing import List
from urllib.parse import urljoin

import bs4
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://realtylink.org/en/properties~for-rent?uc=0"
LIST_OF_ALL_LINKS: List[str] = []
HEADERS = {
        "Referer": "https://realtylink.org/en/properties~for-rent?uc=0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36"
                      " (KHTML, like Gecko) Chrome/000000000 Safari/537.36",
    }


def get_all_links_from_page(url: str) -> list | str:
    """
    Extracts all links from a given page.

    Args:
        url (str): The URL of the page.

    Returns:
        list | str: A list of links extracted from the page.
    """
    base_url = "https://realtylink.org"

    response = requests.get(url, headers=HEADERS)
    html_text = response.text
    soup = bs4.BeautifulSoup(html_text, "html.parser")

    description_divs = soup.find_all("a", class_="a-more-detail")
    list_of_links = []
    if description_divs:
        for description_div in description_divs:
            href_value = description_div.get("href")
            full_link = urljoin(base_url, href_value)
            list_of_links.append(full_link)
    if list_of_links:
        return list_of_links
    else:
        return "Elements <a class='a-more-detail'> not found."


def scrape_links_with_selenium(url: str, num_pages: int = 3):
    """
    Scrapes links using Selenium from multiple pages.

    Args:
        url (str): The URL of the page to start scraping.
        num_pages (int, optional): The number of pages to scrape.
            Defaults to 3.
    """
    driver = webdriver.Chrome()

    try:
        for _ in range(num_pages):
            driver.get(url)
            LIST_OF_ALL_LINKS.extend(get_all_links_from_page(url))
            next_button = driver.find_element(By.CLASS_NAME, "next")
            next_button.click()

    finally:
        driver.quit()


scrape_links_with_selenium(URL)
