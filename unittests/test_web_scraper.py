from unittest import mock

from web_scraper import *


def test_search_vital():
    my_bike = Bike
    my_bike.brand = "YT"
    my_bike.model = "CAPRA 2022"
    expected_output = [['2022 YT Capra MX Launch Edition',
                        'https://www.vitalmtb.com/product/guide/Bikes,3/YT/Capra-MX-Launch-Edition,33908'],
                       ['2022 YT Capra MX Core 4',
                        'https://www.vitalmtb.com/product/guide/Bikes,3/YT/Capra-MX-Core-4,33909'],
                       ['2022 YT Capra 29 Uncaged 6',
                        'https://www.vitalmtb.com/product/guide/Bikes,3/YT/Capra-29-Uncaged-6,35144'],
                       ['2022 YT Capra 29 Core 4',
                        'https://www.vitalmtb.com/product/guide/Bikes,3/YT/Capra-29-Core-4,33911'],
                       ['2022 YT Capra 29 Core 3',
                        'https://www.vitalmtb.com/product/guide/Bikes,3/YT/Capra-29-Core-3,33912'],
                       ['2022 YT Capra MX Core 3',
                        'https://www.vitalmtb.com/product/guide/Bikes,3/YT/Capra-MX-Core-3,33910'],
                       ['YT Mountain Bikes',
                        'https://www.vitalmtb.com/product/combination/YBMC/2022/YT,1088/Bikes,3/Capra'],
                       ['2022 YT Jeffsy 29 Uncaged 6',
                        'https://www.vitalmtb.com/product/guide/Bikes,3/YT/Jeffsy-29-Uncaged-6,35143'],
                       ['2020 YT Capra Elite 29',
                        'https://www.vitalmtb.com/product/guide/Bikes,3/YT/Capra-Elite-29,30869']]
    with open("test_html/search?cat=Site&page=1&period=all_time&q=YT+CAPRA+2022&section=product") as f:
        mocked_web_page = f.read()
    with mock.patch('web_scraper.get_page', return_value=mocked_web_page):
        output = search_bike_vital(my_bike)
    assert output == expected_output

