import datetime
from dataclasses import dataclass
from typing import Optional

from enum import Enum


# the __init__ allows to create BikeData @dataclass with not specifying all arguments
# trying to access not specified argument of instance of class will result in attribute error
@dataclass
class BikeData:
    def __init__(self, *args, **kwargs):
        counter = 0
        args_counter = 0
        while args_counter < len(args):
            current_attr_name = list(self.__annotations__.keys())[counter]
            if current_attr_name in kwargs.keys():
                self.__setattr__(current_attr_name, kwargs.pop(current_attr_name))
            else:
                self.__setattr__(current_attr_name, args[args_counter])
                args_counter += 1
            counter += 1
        for arg, value in kwargs.items():
            self.__setattr__(arg, value)


class SuspensionType(Enum):
    AIR = "air"
    SPRING = "spring"


# TODO: re-check standards
class HeadsetStandard(Enum):
    TAPERED = "tapered"
    AHEAD = "ahead"
    THREADED = "threaded"
    INTEGRATED = "integrated"
    INTEGRATED_PRESS_FIT = "integrated press fit"


class BottomBracketStandards(Enum):
    THREADED = "threaded"
    PRESS_FIT = "press fit"
    BB30 = "BB30"
    ISIS = "ISIS"
    SQUARE = "square"


class Usage(BikeData):
    hours: datetime
    distance: Optional[float]
    races: Optional[int]


class Geometry(BikeData):
    top_tube_length: Optional[int]
    head_tube_angle: Optional[int]
    head_tube_length: Optional[int]
    seat_tube_angle: Optional[int]
    seat_tube_length: Optional[int]
    bottom_bracket_height: Optional[int]
    bottom_bracket_drop: Optional[int]
    chainstay_length: Optional[int]
    wheelbase: Optional[int]
    standover_height: Optional[int]
    reach: Optional[int]
    stack: Optional[int]


class Component(BikeData):
    brand: Optional[str]
    model: Optional[str]
    usage: Usage


class Frame(Component):
    model_year: Optional[int]
    size: Optional[str]
    boost: Optional[bool]


class Shock(Component):
    length: {int, str}  # {value, units}
    suspension_type: SuspensionType


class Fork(Component):
    travel: Optional[int]
    boost: Optional[bool]
    offset: Optional[int]


class Handlebars(Component):
    width: Optional[int]
    diameter: Optional[int]


class Stem(Component):
    length: Optional[int]
    rise: Optional[int]
    diameter: Optional[int]


class Headset(Component):
    standard: HeadsetStandard


class Grips(Component):
    pass


class BreakDisc(Component):
    centerlock: Optional[bool]
    diameter: Optional[int]

    @property
    def diameter(self):
        return self.diameter

    @diameter.setter
    def diameter(self, value):
        if value in [140, 160, 180, 200, 203, 220]:
            self.diameter = value
        else:
            raise ValueError


class Pads(Component):
    compound: Optional[str]


class Break(Component):
    pass


class VBreak(Break):
    pass


class DiscBreak(Break):
    disc: BreakDisc
    pads: Pads


def wheel_diameter_check(value):
    diameter = 27.5 if value == "650B" else value
    if diameter not in [20, 24, 26, 27.5, 29]:
        raise ValueError
    return diameter


class Rim(Component):
    spoke_count: Optional[int]
    diameter: Optional[str]

    @property
    def diameter(self):
        return self.diameter

    @diameter.setter
    def diameter(self, value):
        self.diameter = wheel_diameter_check(value)


class Hub(Component):
    holes_count: Optional[int]
    boost: Optional[bool]


class Tyre(Component):
    width: Optional[float]
    casing: Optional[str]
    compound: Optional[str]
    diameter: Optional[int]

    @property
    def diameter(self):
        return self.diameter

    @diameter.setter
    def diameter(self, value):
        self.diameter = wheel_diameter_check(value)


class Wheel(Component):
    rim: Rim
    hub: Hub
    tyre: Tyre
    diameter: Optional[int]

    @property
    def diameter(self):
        if self.rim.diameter:
            if self.rim.diameter != self.diameter:
                raise ValueError("Rim diameter differs from wheel diameter!")
        if self.tyre.diameter:
            if self.tyre.diameter != self.diameter:
                raise ValueError("Tyre diameter differs from wheel diameter!")
        return self.diameter

    @diameter.setter
    def diameter(self, value):
        if self.rim.diameter:
            if self.rim.diameter != value:
                raise ValueError(f"Rim diameter {self.rim.diameter} differs from provided value!")
        if self.tyre.diameter:
            if self.tyre.diameter != value:
                raise ValueError(f"Tyre diameter {self.tyre.diameter} differs from from provided value!")
        self.diameter = wheel_diameter_check(value)


class BottomBracket(Component):
    standard = BottomBracketStandards


class Cranks(Component):
    length: Optional[int]
    boost: Optional[bool]


class Pedals(Component):
    pass


class Chainring(Component):
    tooth_number: Optional[int]
    offset: Optional[int]


class Cassette(Component):
    speeds: Optional[int]
    tooth_range: Optional[str]  # might be divided into low and high with int values


class Derailleur(Component):
    speeds: Optional[int]


class Chain(Component):
    speeds_compatibility: Optional[int]


class Saddle(Component):
    pass


class Seatpost(Component):
    telescopic: Optional[bool]
    diameter: Optional[float]
    travel: Optional[int]


class BikeComponents(BikeData):
    frame: Optional[Frame]
    shock: Optional[Shock]
    fork: Optional[Fork]
    handlebars: Optional[Handlebars]
    stem: Optional[Stem]
    headset: Optional[Headset]
    grips: Optional[Grips]
    front_break: Optional[Break]
    rear_break: Optional[Break]
    front_wheel: Optional[Wheel]
    rear_wheel: Optional[Wheel]
    bottom_bracket: Optional[BottomBracket]
    cranks: Optional[Cranks]
    pedals: Optional[Pedals]
    chainring: Optional[Chainring]
    cassette: Optional[Cassette]
    derailleur: Optional[Derailleur]
    chain: Optional[Chain]
    saddle: Optional[Saddle]
    seatpost: Optional[Seatpost]


class PressureUnits(Enum):
    PSI = "psi"
    BAR = "bar"


class Pressure:
    value: Optional[int]
    units: Optional[PressureUnits]


class SuspensionSetup(BikeData):
    pressure: Optional[Pressure]
    fast_compression: Optional[int]
    low_compression: Optional[int]
    fast_rebound: Optional[int]
    low_rebound: Optional[int]


class BikeSetup(BikeData):
    front_tyre: Optional[Pressure]
    rear_tyre: Optional[Pressure]
    fork: Optional[SuspensionSetup]
    shock: Optional[SuspensionSetup]
    stem_height: Optional[int]
    saddle_height: Optional[int]
    brake_levers_angle: Optional[int]
    chain_length: Optional[int]
    chainline: Optional[int]


class Bike(BikeData):
    users_name: Optional[str]
    brand: Optional[str]
    model: Optional[str]
    model_year: Optional[int]
    purchase_date: Optional[datetime.time]
    total_usage: Optional[Usage]
    geometry: Optional[Geometry]
    components: Optional[BikeComponents]
    setup: Optional[BikeSetup]
