"""
This file should contain classes for scraping following information:
* possible automatic gathering bike information (components, geometry) from provided web pages
* searching for replacement parts
* checking the price and availability of parts in wishlist
"""
from bs4 import BeautifulSoup
import lxml
import requests

from bike_data import Bike

VITAL_MTB_SEARCH = "https://www.vitalmtb.com/search?cat=Site&page=1&period=all_time&q={}&section=product"
BIKE_PRODUCT_SEPARATORS = [" Bike -", " -"]


def get_page(url_link: str):
    response = requests.get(VITAL_MTB_SEARCH.format(url_link))
    response.raise_for_status()
    return response.text


def search_bike_vital(bike: Bike) -> list:
    search_by = bike.brand.split() + bike.model.split()
    link_search = "+".join(search_by)
    html_page = get_page(link_search)
    soup = BeautifulSoup(html_page, features="lxml")
    found_items = [found_item.find("a") for found_item in soup.find_all(role="search-result")]

    results = []
    for item in found_items:
        text = item.text
        link = item["href"]
        if any([x.lower() in text.lower() for x in search_by]):
            for product_string in BIKE_PRODUCT_SEPARATORS:
                if product_string in text:
                    results.append([text.split(product_string)[0], link])
                    break
    return results
