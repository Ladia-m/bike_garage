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
        assert hasattr(test_bike.total_usage, "hours")
        assert hasattr(test_bike.total_usage, "distance")
        assert hasattr(test_bike.total_usage, "races")
        assert hasattr(test_bike, "geometry")
        assert hasattr(test_bike.geometry, "top_tube_length")
        assert hasattr(test_bike.geometry, "head_tube_angle")
        assert hasattr(test_bike.geometry, "head_tube_length")
        assert hasattr(test_bike.geometry, "seat_tube_angle")
        assert hasattr(test_bike.geometry, "seat_tube_length")
        assert hasattr(test_bike.geometry, "bottom_bracket_height")
        assert hasattr(test_bike.geometry, "bottom_bracket_drop")
        assert hasattr(test_bike.geometry, "chainstay_length")
        assert hasattr(test_bike.geometry, "wheelbase")
        assert hasattr(test_bike.geometry, "standover")
        assert hasattr(test_bike.geometry, "reach")
        assert hasattr(test_bike.geometry, "stack")
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
        assert hasattr(test_bike.setup, "front_tyre")
        assert hasattr(test_bike.setup, "rear_tyre")
        assert hasattr(test_bike.setup, "fork")
        assert hasattr(test_bike.setup.fork, "pressure")
        assert hasattr(test_bike.setup.fork, "fast_compression")
        assert hasattr(test_bike.setup.fork, "low_compression")
        assert hasattr(test_bike.setup.fork, "fast_rebound")
        assert hasattr(test_bike.setup.fork, "low_rebound")
        assert hasattr(test_bike.setup, "shock")
        assert hasattr(test_bike.setup.shock, "pressure")
        assert hasattr(test_bike.setup.shock, "fast_compression")
        assert hasattr(test_bike.setup.shock, "low_compression")
        assert hasattr(test_bike.setup.shock, "fast_rebound")
        assert hasattr(test_bike.setup.shock, "low_rebound")
        assert hasattr(test_bike.setup, "stem_height")
        assert hasattr(test_bike.setup, "saddle_height")
        assert hasattr(test_bike.setup, "brake_levers_angle")
        assert hasattr(test_bike.setup, "chain_length")
        assert hasattr(test_bike.setup, "chainline")
        assert hasattr(test_bike, "weight")

    def test_init_bike_builder_with_bike(self):
        users_name_value = "test bike"
        brand_value = "TB"
        model_value = "tester"
        model_year_value = "2020"
        test_bike = Bike(users_name=users_name_value, brand=brand_value, model=model_value, model_year=model_year_value)

        test_bike.geometry = Geometry()
        top_tube_length_value = 630
        head_tube_angle_value = 64
        head_tube_length_value = 120
        seat_tube_angle_value = 77.4
        seat_tube_length_value = 470
        bottom_bracket_drop_value = {30, 12}
        reach_value = 484
        test_bike.geometry.top_tube_length = top_tube_length_value
        test_bike.geometry.head_tube_angle = head_tube_angle_value
        test_bike.geometry.head_tube_length = head_tube_length_value
        test_bike.geometry.seat_tube_angle = seat_tube_angle_value
        test_bike.geometry.seat_tube_length = seat_tube_length_value
        test_bike.geometry.bottom_bracket_drop = bottom_bracket_drop_value
        test_bike.geometry.reach = reach_value

        assert test_bike.users_name == users_name_value
        assert test_bike.brand == brand_value
        assert test_bike.model == model_value
        assert test_bike.model_year == model_year_value
        assert hasattr(test_bike, "purchase_date")
        assert hasattr(test_bike, "geometry")
        assert hasattr(test_bike, "total_usage")
        assert hasattr(test_bike, "setup")
        assert hasattr(test_bike, "components")
        assert hasattr(test_bike, "weight")

        with pytest.raises(AttributeError):
            test_bike.components.wheels.rear_wheel.hub.brand = "DT Swiss"

        try:
            test_builder = BikeBuilder(bike=test_bike)
            test_bike.components.wheels.rear_wheel.hub.brand = "DT Swiss"
        except AttributeError:
            pytest.fail("Attributes of Bike object are not initialized as expected.")

        assert test_bike.geometry.top_tube_length == top_tube_length_value
        assert test_bike.geometry.head_tube_angle == head_tube_angle_value
        assert test_bike.geometry.head_tube_length == head_tube_length_value
        assert test_bike.geometry.seat_tube_angle == seat_tube_angle_value
        assert test_bike.geometry.seat_tube_length == seat_tube_length_value
        assert test_bike.geometry.bottom_bracket_drop == bottom_bracket_drop_value
        assert test_bike.geometry.reach == reach_value
        assert test_bike.geometry.bottom_bracket_height is None
        assert test_bike.geometry.chainstay_length is None
        assert test_bike.geometry.wheelbase is None
        assert test_bike.geometry.standover is None
        assert test_bike.geometry.stack is None

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
