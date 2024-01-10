## RealtyLink Scraper
This project is a scraper for the real estate website realtylink.org. The script is written in Python and is designed to retrieve information about ads of the "Residental: For Rent". The scraper collects data from 60 ads and creates a JSON file with the specified parameters for each ad.

## Installing / Getting started:
```shell
To get started, you need to clone the repository from GitHub: https://github.com/Morty67/parser_for_jooble/tree/developer
Python 3.11.3 must be installed

python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)

pip install -r requirements.txt
```
## Properties of the ad object:
*  Link to the ad
*  Title of the ad
*  Region
*  Address.
*  Description.
*  An array of images
*  Price of the room
*  Number of rooms
*  The area of the property

## How to run

```shell
python parser.py
```