import datetime
import typing
from dataclasses import dataclass, field
from typing import Optional, get_origin, Union

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


class BottomBracketStandard(Enum):
    THREADED = "threaded"
    PRESS_FIT = "press fit"
    BB30 = "BB30"
    ISIS = "ISIS"
    SQUARE = "square"


class ISCGStandard(Enum):
    ISCGOLD = "ISCGold"
    ISCG05 = "ISCG05"


class Usage(BikeData):
    hours: datetime.time = field(default=0)
    distance: float = field(default=0)
    races: int = field(default=0)


class Geometry(BikeData):
    top_tube_length: Optional[int]
    head_tube_angle: Optional[Union[int, set]]
    head_tube_length: Optional[int]
    seat_tube_angle: Optional[Union[int, set]]
    seat_tube_length: Optional[int]
    bottom_bracket_height: Optional[Union[int, set]]
    bottom_bracket_drop: Optional[Union[int, set]]
    chainstay_length: Optional[int]
    wheelbase: Optional[int]
    standover: Optional[int]
    reach: Optional[int]
    stack: Optional[int]


class Component(BikeData):
    brand: Optional[str]
    model: Optional[str]
    usage: Usage


class Frame(Component):
    model_year: Optional[int]
    size: Optional[str]
    dropout: Optional[int]
    travel: Optional[int]
    head_tube: Optional[HeadsetStandard]
    iscg_tabs: Optional[ISCGStandard]


class Shock(Component):
    length: Optional[int]
    suspension_type: Optional[SuspensionType]


class Fork(Component):
    travel: Optional[int]
    dropout: Optional[int]
    offset: Optional[int]


class Handlebars(Component):
    width: Optional[int]
    diameter: Optional[int]


class Stem(Component):
    length: Optional[int]
    rise: Optional[int]
    diameter: Optional[int]


class Headset(Component):
    standard: Optional[HeadsetStandard]


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


class WheelSize(Enum):
    SIXTEEN = "16\""
    TWENTY = "20\""
    TWENTY_FOUR = "24\""
    TWENTY_SIX = "26\""
    TWENTY_SEVEN = "27,5\"_650B"
    TWENTY_NINE = "29\""
    MULLET = "mullet_mixed"


class Rim(Component):
    spoke_count: Optional[int]
    size: Optional[WheelSize]


class Hub(Component):
    holes_count: Optional[int]
    boost: Optional[bool]


class Tyre(Component):
    width: Optional[float]
    casing: Optional[str]
    compound: Optional[str]
    size: Optional[WheelSize]


class Wheel(Component):
    rim: Rim
    hub: Hub
    tyre: Tyre
    size: Optional[WheelSize]


class Wheels(Component):
    size: Optional[WheelSize]
    front_wheel: Wheel
    rear_wheel: Wheel

    @property
    def size(self):
        return self.size

    @size.setter
    def size(self, value: WheelSize):
        if value == WheelSize.MULLET:
            self.front_wheel.size = WheelSize.TWENTY_NINE
            self.rear_wheel.size = WheelSize.TWENTY_SEVEN
        else:
            self.front_wheel.size = value
            self.rear_wheel.size = value


class BottomBracket(Component):
    standard = Optional[BottomBracketStandard]


class Cranks(Component):
    length: Optional[int]
    boost: Optional[bool]


class Pedals(Component):
    pass


class Chainguide(Component):
    mounting: Optional[str]


class Chainrings(Component):
    number_of_chainrings: Optional[int]
    tooth_numbers: Optional[list]
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
    frame: Frame
    shock: Shock
    fork: Fork
    handlebars: Handlebars
    stem: Stem
    headset: Headset
    grips: Grips
    front_break: Break
    rear_break: Break
    wheels: Wheels
    bottom_bracket: BottomBracket
    cranks: Cranks
    pedals: Pedals
    chainguide: Chainguide
    chainring: Chainrings
    cassette: Cassette
    derailleur: Derailleur
    chain: Chain
    saddle: Saddle
    seatpost: Seatpost


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
    fork: SuspensionSetup
    shock: SuspensionSetup
    stem_height: Optional[int]
    saddle_height: Optional[int]
    brake_levers_angle: Optional[int]
    chain_length: Optional[int]
    chainline: Optional[int]


class Bike(BikeData):
    # TODO: generate ID of bike
    users_name: str = field(default=None)
    brand: str = field(default=None)
    model: str = field(default=None)
    model_year: str = field(default=None)
    purchase_date: datetime.time = field(default=datetime.datetime.now())
    total_usage: Usage
    geometry: Geometry
    components: BikeComponents
    setup: BikeSetup
    weight: int = field(default=None)  # TODO: find weight module
