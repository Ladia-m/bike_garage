"""
This file should contain classes for scraping following information:
* possible automatic gathering bike information (components, geometry) from provided web pages
* searching for replacement parts
* checking the price and availability of parts in wishlist
"""
from bs4 import BeautifulSoup
import lxml
import requests

from bike_data import *

VITAL_MTB_SEARCH = "https://www.vitalmtb.com/search?cat=Site&page=1&period=all_time&q={}&section=product"
BIKE_PRODUCT_SEPARATORS = [" Bike -", " -"]


def get_page(url_link: str):
    response = requests.get(VITAL_MTB_SEARCH.format(url_link))
    response.raise_for_status()
    return response.text


def search_bike_vital(bike: Bike) -> list:
    search_by = bike.brand.split() + bike.model.split()
    link_search = "+".join(search_by)
    search_result_html = get_page(link_search)
    soup = BeautifulSoup(search_result_html, features="lxml")
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


def find_specs_vital(bike: Bike, link: str):
    bike_page_html = get_page(link)
    soup = BeautifulSoup(bike_page_html, features="lxml")
    specs_table = soup.find_all("table", {"class": "specs"})[0]
    attr_setter = {"Product": lambda bike_instance, data: product_setter(bike_instance, data),
                   "Model Year": lambda bike_instance, data: model_year_setter(bike_instance, data),
                   "Wheel Size": lambda bike_instance, data: wheel_size_setter(bike_instance, data),
                   "Rear Travel": lambda bike_instance, data: frame_travel_setter(bike_instance, data),
                   "Rear Shock": lambda bike_instance, data: shock_setter(bike_instance, data),
                   "Fork": lambda bike_instance, data: fork_setter(bike_instance, data),
                   "Fork Travel": lambda bike_instance, data: fork_travel_setter(bike_instance, data),
                   "Head Tube Diameter": lambda bike_instance, data: head_tube_setter(bike_instance, data),
                   "Headset": lambda bike_instance, data: headset_setter(bike_instance, data),
                   "Handlebar": lambda bike_instance, data: handlebar_setter(bike_instance, data),
                   "Stem": lambda bike_instance, data: stem_setter(bike_instance, data),
                   "Grips": lambda bike_instance, data: grips_setter(bike_instance, data),
                   "Brakes": lambda bike_instance, data: brakes_setter(bike_instance, data),
                   "Shifters": lambda bike_instance, data: shifters_setter(bike_instance, data),
                   "Front Derailleur": lambda bike_instance, data: front_derailleur_setter(bike_instance, data),
                   "Rear Derailleur": lambda bike_instance, data: rear_derailleur_setter(bike_instance, data),
                   "ISCG Tabs": lambda bike_instance, data: iscg_tabs_setter(bike_instance, data),
                   "Chainguide": lambda bike_instance, data: chainguide_setter(bike_instance, data),
                   "Cranks": lambda bike_instance, data: cranks_setter(bike_instance, data),
                   "Chainrings": lambda bike_instance, data: chainrings_setter(bike_instance, data),
                   "Bottom Bracket	": lambda bike_instance, data: bottom_bracket_setter(bike_instance, data),
                   "Pedals	": lambda bike_instance, data: pedals_setter(bike_instance, data),
                   "Chain": lambda bike_instance, data: chain_setter(bike_instance, data),
                   "Cassette": lambda bike_instance, data: cassette_setter(bike_instance, data),
                   "Rims": lambda bike_instance, data: rims_setter(bike_instance, data),
                   "Hubs": lambda bike_instance, data: hubs_setter(bike_instance, data),
                   "Tires": lambda bike_instance, data: tires_setter(bike_instance, data),
                   "Saddle": lambda bike_instance, data: saddle_setter(bike_instance, data),
                   "Seatpost": lambda bike_instance, data: seatpost_setter(bike_instance, data),
                   "Seatpost Diameter": lambda bike_instance, data: seatpost_diameter_setter(bike_instance, data),
                   "Rear Dropout / Hub Dimensions": lambda bike_instance, data: dropout_setter(bike_instance, data),
                   "Weight": lambda bike_instance, data: weight_setter(bike_instance, data),
                   }

    for row in specs_table.find_all("tr"):
        if not row.find("th"):
            continue
        heading = row.find("th").text
        if heading not in attr_setter:
            continue
        if "Sizes and Geometry" in heading:
            pass
            # bike.geometry = parse_geometry_table(row.find("table", {"class": "product-specs"}))
        attr_setter[heading](bike, row.find("td").get_text("\n").strip())

    return bike


def product_setter(bike: Bike, data: str) -> Bike:
    bike.brand, bike.model = data.split(' ', 1)
    return bike


def model_year_setter(bike: Bike, data: str) -> Bike:
    if int(data):
        bike.model_year = int(data)
    return bike


def wheel_size_setter(bike: Bike, data: str) -> Bike:
    if isinstance(bike.components.wheels.size, WheelSize):  # This needs to use isinstance because of @property usage
        return bike
    if "mullet" in data or "mixed" in data:
        bike.components.wheels.size = WheelSize.MULLET
    if "29" in data:
        bike.components.wheels.size = WheelSize.TWENTY_NINE
    if "27" in data or "650B" in data:
        bike.components.wheels.size = WheelSize.TWENTY_SEVEN
    if "27" in data and "29" in data:
        bike.components.wheels.size = WheelSize.TWENTY_NINE_MULLET
    if "26" in data:
        bike.components.wheels.size = WheelSize.TWENTY_SIX
    if "24" in data:
        bike.components.wheels.size = WheelSize.TWENTY_FOUR
    if "20" in data:
        bike.components.wheels.size = WheelSize.TWENTY
    if "16" in data:
        bike.components.wheels.size = WheelSize.SIXTEEN
    return bike


def frame_travel_setter(bike: Bike, data: str) -> Bike:
    bike.components.frame.travel = int(data.rstrip("mm"))
    return bike


def shock_setter(bike: Bike, data: str) -> Bike:
    bike.components.shock = default_component_setter(bike.components.shock, data)
    return bike


def fork_setter(bike: Bike, data: str) -> Bike:
    data = data.replace("\n", ", ").split(", ")
    bike.components.fork.name = data[0]
    if len(data) > 1:
        for item in data[1:]:
            if "offset" in item:
                bike.components.fork.offset = int(item.replace("offset", "").strip().strip("mm"))
                data.remove(item)
                break
        bike.components.fork.additional_info = ", ".join(data[1:])
    return bike


def fork_travel_setter(bike: Bike, data: str) -> Bike:
    bike.components.fork.travel = int(data.rstrip("mm"))
    return bike


def head_tube_setter(bike: Bike, data: str) -> Bike:
    for standard in HeadsetStandard:
        if standard.value in data.lower():
            bike.components.headset.standard = standard
            bike.components.frame.head_tube = standard
            break
    return bike


def headset_setter(bike: Bike, data: str) -> Bike:
    bike.components.headset = default_component_setter(bike.components.headset, data)
    return bike


def handlebar_setter(bike: Bike, data: str) -> Bike:
    data = data.replace("\n", ", ").split(", ")
    bike.components.handlebars.name = data[0]
    additional_info = []
    for item in data[1:]:
        if "width" in item.lower():
            bike.components.handlebars.width = int(item.split("mm")[0].split()[-1])
        elif "diameter" in item.lower():
            bike.components.handlebars.diameter = int(item.split("mm")[0].split()[-1])
        elif "rise" in item.lower():
            bike.components.handlebars.rise = int(item.split("mm")[0].split()[-1])
        else:
            additional_info.append(item)
    bike.components.handlebars.additional_info = ", ".join(additional_info) if len(additional_info) > 0 else None
    return bike


def stem_setter(bike: Bike, data: str) -> Bike:
    data = data.replace("\n", ", ").split(", ")
    bike.components.stem.name = data[0]
    additional_info = []
    for item in data[1:]:
        if "length" in item.lower():
            bike.components.stem.length = int(item.split("mm")[0].split()[-1])
        elif "bar clamp" in item.lower():
            bike.components.stem.bar_clamp = int(item.split("mm")[0].split()[-1])
        elif "rise" in item.lower():
            bike.components.stem.rise_angle = int(item.split("°")[0].split()[-1])
        else:
            additional_info.append(item)
    bike.components.handlebars.additional_info = ", ".join(additional_info) if len(additional_info) > 0 else None
    return bike


def grips_setter(bike: Bike, data: str) -> Bike:
    data = data.split(", ")
    bike.components.grips.name = data[0]
    for item in data:
        if "lock" in item:
            bike.components.grips.lock_on = True
            data.remove(item)
    if len(data) > 1:
        bike.components.grips.additional_info = ", ".join(data[1:])
    return bike


def brakes_setter(bike: Bike, data: str) -> Bike:
    data = data.replace("\n", ", ").split(", ")
    additional_info = []
    for item in data[1:]:
        if "rotors" in item.lower():
            bike.components.breaks.front_break = DiscBreak(disc=BreakDisc())
            bike.components.breaks.front_break.disc.diameter = int(item.split("mm")[0].split()[-1])
            bike.components.breaks.rear_break = DiscBreak(disc=BreakDisc())
            bike.components.breaks.rear_break.disc.diameter = int(item.split("mm")[0].split()[-1])
            if "centerline" in item.lower():
                bike.components.breaks.front_break.disc.centerlock = True
                bike.components.breaks.rear_break.disc.centerlock = True
        elif "rotor" in item.lower():
            if "front" in item.lower():
                bike.components.breaks.front_break = DiscBreak(disc=BreakDisc())
                bike.components.breaks.front_break.disc.diameter = int(item.split("mm")[0].split()[-1])
            if "rear" in item.lower():
                bike.components.breaks.rear_break = DiscBreak(disc=BreakDisc())
                bike.components.breaks.rear_break.disc.diameter = int(item.split("mm")[0].split()[-1])
            if "centerline" in item.lower():
                bike.components.breaks.front_break.disc.centerlock = True
                bike.components.breaks.rear_break.disc.centerlock = True
        else:
            additional_info.append(item)
        bike.components.breaks.front_break.name = data[0]
        bike.components.breaks.rear_break.name = data[0]
        bike.components.breaks.additional_info = ", ".join(additional_info) if len(additional_info) > 0 else None
    return bike


def drivetrain_setter(bike: Bike, data: str) -> Bike:
    pass


def shifters_setter(bike: Bike, data: str) -> Bike:
    pass


def front_derailleur_setter(bike: Bike, data: str) -> Bike:
    pass


def rear_derailleur_setter(bike: Bike, data: str) -> Bike:
    pass


def iscg_tabs_setter(bike: Bike, data: str) -> Bike:
    pass


def chainguide_setter(bike: Bike, data: str) -> Bike:
    pass


def cranks_setter(bike: Bike, data: str) -> Bike:
    pass


def chainrings_setter(bike: Bike, data: str) -> Bike:
    pass


def bottom_bracket_setter(bike: Bike, data: str) -> Bike:
    pass


def pedals_setter(bike: Bike, data: str) -> Bike:
    pass


def chain_setter(bike: Bike, data: str) -> Bike:
    pass


def cassette_setter(bike: Bike, data: str) -> Bike:
    pass


def rims_setter(bike: Bike, data: str) -> Bike:
    pass


def hubs_setter(bike: Bike, data: str) -> Bike:
    pass


def tires_setter(bike: Bike, data: str) -> Bike:
    pass


def saddle_setter(bike: Bike, data: str) -> Bike:
    pass


def seatpost_setter(bike: Bike, data: str) -> Bike:
    pass


def seatpost_diameter_setter(bike: Bike, data: str) -> Bike:
    pass


def dropout_setter(bike: Bike, data: str) -> Bike:
    pass


def weight_setter(bike: Bike, data: str) -> Bike:
    pass


def default_component_setter(component: Component, data: str) -> Component:
    data = data.replace("\n", ", ").split(", ", 1)
    component.name = data[0]
    if len(data) > 1:
        component.additional_info = data[1]
    return component


def parse_geometry_table(geometry_table):
    geometry = Geometry()
    spec_rows = geometry_table.find_all("tr")
    for row in spec_rows:
        heading_text = row.find("th").text
        attribute = None
        if heading_text.lower().replace(" ", "_") in Geometry.__annotations__:
            pass
        if attribute:
            geometry.__setattr__(attribute, row.find("td").text)
    return geometry
