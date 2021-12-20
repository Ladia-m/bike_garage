"""
This file represents classes for building bike objects (later hopefully probably using builder pattern)

Currently I am using pseudo-builder (not builder pattern), I am not sure how to do it properly at this moment.
Hopefully it will be fixed later if I find time
"""

from bike_data import *


class BikeBuilder:
    def __init__(self, bike=None):
        self.bike = bike
        if not bike:
            self.bike = Bike()
        self.init_bike()
        self.init_components()
        self.init_setup()

    def init_bike(self):
        if not self.bike.total_usage:
            self.bike.total_usage = Usage()
        if not self.bike.geometry:
            self.bike.geometry = Geometry()
        if not self.bike.components:
            self.bike.components = BikeComponents()
        if not self.bike.setup:
            self.bike.setup = BikeSetup()

    def init_components(self):
        for attr, _class in self.bike.components.__annotations__.items():
            if getattr(self.bike.components, attr) is not _class:
                self.bike.components.__setattr__(attr, _class)
        self.init_wheels()

    def init_setup(self):
        if not self.bike.setup.fork:
            self.bike.setup.fork = SuspensionSetup()
        if not self.bike.setup.shock:
            self.bike.setup.shock = SuspensionSetup()

    def init_wheels(self):
        if not self.bike.components.wheels.front_wheel:
            self.bike.components.wheels.front_wheel = Wheel()
        self.bike.components.wheels.front_wheel = self.init_wheel(self.bike.components.wheels.front_wheel)
        if not self.bike.components.wheels.rear_wheel:
            self.bike.components.wheels.rear_wheel = Wheel()
        self.bike.components.wheels.rear_wheel = self.init_wheel(self.bike.components.wheels.rear_wheel)

    @staticmethod
    def init_wheel(wheel):
        if not wheel.rim:
            wheel.rim = Rim()
        if not wheel.hub:
            wheel.hub = Hub()
        if not wheel.tyre:
            wheel.tyre = Tyre()
        return wheel

    def get_bike(self):
        return self.bike
