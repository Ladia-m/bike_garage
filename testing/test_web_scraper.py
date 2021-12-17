from unittest import mock, TestCase

from web_scraper import *
from bike_builder import BikeBuilder


class WebScraperTests(TestCase):

    test_bike = Bike()
    test_bike.brand = "YT"
    test_bike.model = "CAPRA 2022"
    bike_builder = BikeBuilder(test_bike)

    @mock.patch('web_scraper.get_page')
    def test_search_vital(self, mock_get_page):
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
        mock_get_page.return_value = mocked_web_page
        output = search_bike_vital(self.test_bike)
        assert output == expected_output

    @mock.patch('web_scraper.get_page')
    def test_find_specs_vital(self, mock_get_page):
        with open("test_html/Capra-MX-Launch-Edition") as f:
            mocked_web_page = f.read()
        mock_get_page.return_value = mocked_web_page
        try:
            find_specs_vital(self.test_bike,
                             'https://www.vitalmtb.com/product/guide/Bikes,3/YT/Capra-MX-Launch-Edition,33908')
        except AttributeError as e:
            raise e
