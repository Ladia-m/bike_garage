from unittest import TestCase

import pytest

from bike_data import *
from bike_builder import BikeBuilder


class TestBikeBuilder(TestCase):

    def test_init_bike_builder_without_bike(self):
        test_builder = BikeBuilder()
        test_bike = test_builder.get_bike()
        assert hasattr(test_bike, "users_name")
        assert hasattr(test_bike, "brand")
        assert hasattr(test_bike, "model")
        assert hasattr(test_bike, "model_year")
        assert hasattr(test_bike, "purchase_date")
        assert hasattr(test_bike, "total_usage")
        assert hasattr(test_bike, "geometry")
        assert hasattr(test_bike, "components")
        assert hasattr(test_bike.components, "frame")
        assert hasattr(test_bike.components, "shock")
        assert hasattr(test_bike.components, "fork")
        assert hasattr(test_bike.components, "handlebars")
        assert hasattr(test_bike.components, "stem")
        assert hasattr(test_bike.components, "headset")
        assert hasattr(test_bike.components, "grips")
        assert hasattr(test_bike.components, "front_break")
        assert hasattr(test_bike.components, "rear_break")
        assert hasattr(test_bike.components, "wheels")
        assert hasattr(test_bike.components.wheels, "front_wheel")
        assert hasattr(test_bike.components.wheels, "rear_wheel")
        assert hasattr(test_bike.components.wheels.front_wheel, "rim")
        assert hasattr(test_bike.components.wheels.front_wheel, "hub")
        assert hasattr(test_bike.components.wheels.front_wheel, "tyre")
        assert hasattr(test_bike.components.wheels.rear_wheel, "rim")
        assert hasattr(test_bike.components.wheels.rear_wheel, "hub")
        assert hasattr(test_bike.components.wheels.rear_wheel, "tyre")
        assert hasattr(test_bike.components, "bottom_bracket")
        assert hasattr(test_bike.components, "cranks")
        assert hasattr(test_bike.components, "pedals")
        assert hasattr(test_bike.components, "chainguide")
        assert hasattr(test_bike.components, "chainring")
        assert hasattr(test_bike.components, "cassette")
        assert hasattr(test_bike.components, "derailleur")
        assert hasattr(test_bike.components, "chain")
        assert hasattr(test_bike.components, "seatpost")
        assert hasattr(test_bike.components, "seatpost")
        assert hasattr(test_bike, "setup")
        assert hasattr(test_bike, "weight")

    def test_init_bike_builder_with_bike(self):
        test_bike = Bike(user_name="test bike", brand="TB", model="tester", model_year="2020")
        test_bike.geometry = Geometry()
        test_bike.geometry.top_tube_length = 630
        test_bike.geometry.head_tube_angle = 64
        test_bike.geometry.head_tube_length = 120
        test_bike.geometry.seat_tube_angle = 77.4
        test_bike.geometry.seat_tube_length = 470
        test_bike.geometry.bottom_bracket_drop = {30, 12}
        test_bike.geometry.reach = 484

        assert hasattr(test_bike, "user_name")
        assert hasattr(test_bike, "brand")
        assert hasattr(test_bike, "model")
        assert hasattr(test_bike, "model_year")
        assert hasattr(test_bike, "purchase_date")
        assert hasattr(test_bike, "geometry")
        assert hasattr(test_bike, "total_usage") is False
        assert hasattr(test_bike, "setup") is False
        assert hasattr(test_bike, "components") is False
        assert hasattr(test_bike, "weight")

        with pytest.raises(AttributeError):
            test_bike.components.wheels.rear_wheel.hub.brand = "DT Swiss"

        try:
            test_builder = BikeBuilder(bike=test_bike)
            test_bike.components.wheels.rear_wheel.hub.brand = "DT Swiss"
        except AttributeError:
            pytest.fail("Attributes of Bike object are not initialized as expected.")

        assert hasattr(test_bike.geometry, "reach")
        assert hasattr(test_bike.geometry, "top_tube_length")
        assert hasattr(test_bike.geometry, "head_tube_angle")
        assert hasattr(test_bike.geometry, "head_tube_length")
        assert hasattr(test_bike.geometry, "seat_tube_angle")
        assert hasattr(test_bike.geometry, "seat_tube_length")
        assert hasattr(test_bike.geometry, "bottom_bracket_drop")
        assert hasattr(test_bike.geometry, "bottom_bracket_height") is False
        assert hasattr(test_bike.geometry, "chainstay_length") is False
        assert hasattr(test_bike.geometry, "wheelbase") is False
        assert hasattr(test_bike.geometry, "standover") is False
        assert hasattr(test_bike.geometry, "stack") is False

    # following tests are included in test_init_bike_builder_without_bike
    # def test_init_components(self):
    #     pass
    #
    # def test_init_setup(self):
    #     pass
    #
    # def test_init_wheels(self):
    #     pass
    #
    # def test_init_wheel(self):
    #     pass
    #
    # def test_get_bike(self):
    #     pass
