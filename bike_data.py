import datetime
from dataclasses import dataclass, field
from typing import Union

from enum import Enum


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


@dataclass
class Usage:
    hours: datetime.time = field(default=0)
    distance: float = field(default=0)
    races: int = field(default=0)


@dataclass
class Geometry:
    top_tube_length: int = field(default=None)
    head_tube_angle: Union[int, set] = field(default=None)
    head_tube_length: int = field(default=None)
    seat_tube_angle: Union[int, set] = field(default=None)
    seat_tube_length: int = field(default=None)
    bottom_bracket_height: Union[int, set] = field(default=None)
    bottom_bracket_drop: Union[int, set] = field(default=None)
    chainstay_length: int = field(default=None)
    wheelbase: int = field(default=None)
    standover: int = field(default=None)
    reach: int = field(default=None)
    stack: int = field(default=None)


@dataclass
class Component:
    brand: str = field(default=None)
    model: str = field(default=None)
    usage: Usage = field(default=None)


@dataclass
class Frame(Component):
    model_year: int = field(default=None)
    size: str = field(default=None)
    dropout: int = field(default=None)
    travel: int = field(default=None)
    head_tube: HeadsetStandard = field(default=None)
    iscg_tabs: ISCGStandard = field(default=None)


@dataclass
class Shock(Component):
    length: int = field(default=None)
    suspension_type: SuspensionType = field(default=None)


@dataclass
class Fork(Component):
    travel: int = field(default=None)
    dropout: int = field(default=None)
    offset: int = field(default=None)


@dataclass
class Handlebars(Component):
    width: int = field(default=None)
    diameter: int = field(default=None)


@dataclass
class Stem(Component):
    length: int = field(default=None)
    rise: int = field(default=None)
    diameter: int = field(default=None)


@dataclass
class Headset(Component):
    standard: HeadsetStandard = field(default=None)


@dataclass
class Grips(Component):
    pass


@dataclass
class BreakDisc(Component):
    centerlock: bool = field(default=None)
    _diameter: int = field(default=None)

    @property
    def diameter(self):
        return self.diameter

    @diameter.setter
    def diameter(self, value):
        if value in [140, 160, 180, 200, 203, 220]:
            self.diameter = value
        else:
            raise ValueError


@dataclass
class Pads(Component):
    compound: str = field(default=None)


@dataclass
class Break(Component):
    pass


@dataclass
class VBreak(Break):
    pass


@dataclass
class DiscBreak(Break):
    disc: BreakDisc = field(default=None)
    pads: Pads = field(default=None)


@dataclass
class WheelSize(Enum):
    SIXTEEN = "16\""
    TWENTY = "20\""
    TWENTY_FOUR = "24\""
    TWENTY_SIX = "26\""
    TWENTY_SEVEN = "27,5\""
    TWENTY_NINE = "29\""
    MULLET = "mullet"
    TWENTY_NINE_MULLET = "29\"/mullet"


@dataclass
class Rim(Component):
    spoke_count: int = field(default=None)
    size: WheelSize = field(default=None)


@dataclass
class Hub(Component):
    holes_count: int = field(default=None)
    boost: bool = field(default=None)


@dataclass
class Tyre(Component):
    width: float = field(default=None)
    casing: str = field(default=None)
    compound: str = field(default=None)
    size: WheelSize = field(default=None)


@dataclass
class Wheel(Component):
    rim: Rim = field(default=None)
    hub: Hub = field(default=None)
    tyre: Tyre = field(default=None)
    size: WheelSize = field(default=None)


@dataclass
class Wheels(Component):
    _size: WheelSize = field(default=None)
    front_wheel: Wheel = field(default=None)
    rear_wheel: Wheel = field(default=None)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value: WheelSize):
        self._size = value
        if value == WheelSize.MULLET:
            self.front_wheel.size = WheelSize.TWENTY_NINE
            self.rear_wheel.size = WheelSize.TWENTY_SEVEN
        elif value == WheelSize.TWENTY_NINE_MULLET:
            self.front_wheel.size = WheelSize.TWENTY_NINE
            self.rear_wheel.size = WheelSize.TWENTY_NINE_MULLET
        else:
            self.front_wheel.size = value
            self.rear_wheel.size = value


@dataclass
class BottomBracket(Component):
    standard: BottomBracketStandard = field(default=None)


@dataclass
class Cranks(Component):
    length: int = field(default=None)
    boost: bool = field(default=None)


@dataclass
class Pedals(Component):
    pass


@dataclass
class Chainguide(Component):
    mounting: str = field(default=None)


@dataclass
class Chainrings(Component):
    number_of_chainrings: int = field(default=None)
    tooth_numbers: list = field(default=None)
    offset: int = field(default=None)


@dataclass
class Cassette(Component):
    speeds: int = field(default=None)
    tooth_range: str = field(default=None)  # might be divided into low and high with int values


@dataclass
class Derailleur(Component):
    speeds: int = field(default=None)


@dataclass
class Chain(Component):
    speeds_compatibility: int = field(default=None)


@dataclass
class Saddle(Component):
    pass


@dataclass
class Seatpost(Component):
    telescopic: bool = field(default=None)
    diameter: float = field(default=None)
    travel: int = field(default=None)


@dataclass
class BikeComponents:
    frame: Frame = field(default=None)
    shock: Shock = field(default=None)
    fork: Fork = field(default=None)
    handlebars: Handlebars = field(default=None)
    stem: Stem = field(default=None)
    headset: Headset = field(default=None)
    grips: Grips = field(default=None)
    front_break: Break = field(default=None)
    rear_break: Break = field(default=None)
    wheels: Wheels = field(default=None)
    bottom_bracket: BottomBracket = field(default=None)
    cranks: Cranks = field(default=None)
    pedals: Pedals = field(default=None)
    chainguide: Chainguide = field(default=None)
    chainring: Chainrings = field(default=None)
    cassette: Cassette = field(default=None)
    derailleur: Derailleur = field(default=None)
    chain: Chain = field(default=None)
    saddle: Saddle = field(default=None)
    seatpost: Seatpost = field(default=None)


class PressureUnits(Enum):
    PSI = "psi"
    BAR = "bar"


class Pressure:
    value: int = field(default=None)
    units: PressureUnits = field(default=None)


@dataclass
class SuspensionSetup:
    pressure: Pressure = field(default=None)
    fast_compression: int = field(default=None)
    low_compression: int = field(default=None)
    fast_rebound: int = field(default=None)
    low_rebound: int = field(default=None)


@dataclass
class BikeSetup:
    front_tyre: Pressure = field(default=None)
    rear_tyre: Pressure = field(default=None)
    fork: SuspensionSetup = field(default=None)
    shock: SuspensionSetup = field(default=None)
    stem_height: int = field(default=None)
    saddle_height: int = field(default=None)
    brake_levers_angle: int = field(default=None)
    chain_length: int = field(default=None)
    chainline: int = field(default=None)


@dataclass
class Bike:
    # TODO: generate ID of bike
    users_name: str = field(default=None)
    brand: str = field(default=None)
    model: str = field(default=None)
    model_year: str = field(default=None)
    purchase_date: datetime.time = field(default=datetime.datetime.now())
    total_usage: Usage = field(default=None)
    geometry: Geometry = field(default=None)
    components: BikeComponents = field(default=None)
    setup: BikeSetup = field(default=None)
    weight: int = field(default=None)  # TODO: find weight module
