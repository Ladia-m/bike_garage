import datetime
from dataclasses import dataclass

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


class BottomBracketStandards(Enum):
    THREADED = "threaded"
    PRESS_FIT = "press fit"
    BB30 = "BB30"
    ISIS = "ISIS"
    SQUARE = "square"


@dataclass
class Usage:
    hours: datetime
    distance: float
    races: int


@dataclass
class Geometry:
    top_tube: int
    reach: int
    stack: int
    seat_tube: int
    chainstay: int
    head_tube_angle: int
    seat_tube_ange: int
    bb_drop: int
    bb_height: int
    wheelbase: int
    head_tube: int
    standover_height: int


@dataclass
class Component:
    brand: str
    model: str
    usage: Usage


@dataclass
class Frame(Component):
    model_year: int
    size: str
    boost: bool


@dataclass
class Shock(Component):
    length: {int, str}  # {value, units}
    suspension_type: SuspensionType


@dataclass
class Fork(Component):
    travel: int
    boost: bool


@dataclass
class Handlebars(Component):
    width: int
    diameter: int


@dataclass
class Stem(Component):
    length: int
    rise: int
    diameter: int


@dataclass
class Headset(Component):
    standard: HeadsetStandard


@dataclass
class Grips(Component):
    pass


@dataclass
class BreakDisc(Component):
    diameter: int
    centerlock: bool

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
    compound: str


@dataclass
class Break(Component):
    pass


@dataclass
class VBreak(Break):
    pass


@dataclass
class DiscBreak(Break):
    disc: BreakDisc
    pads: Pads


def wheel_diameter_check(value):
    diameter = 27.5 if value == "650B" else value
    if diameter not in [20, 24, 26, 27.5, 29]:
        raise ValueError
    return diameter


@dataclass
class Rim(Component):
    diameter: str
    spoke_count: int

    @property
    def diameter(self):
        return self.diameter

    @diameter.setter
    def diameter(self, value):
        self.diameter = wheel_diameter_check(value)


@dataclass
class Hub(Component):
    holes_count: int
    boost: bool


@dataclass
class Tyre(Component):
    width: float
    casing: str
    compound: str
    diameter: int

    @property
    def diameter(self):
        return self.diameter

    @diameter.setter
    def diameter(self, value):
        self.diameter = wheel_diameter_check(value)


@dataclass
class Wheel(Component):
    rim: Rim
    hub: Hub
    tyre: Tyre
    diameter: int

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


@dataclass
class BottomBracket(Component):
    standard = BottomBracketStandards


@dataclass
class Cranks(Component):
    length: int
    boost: bool


@dataclass
class Pedals(Component):
    pass


@dataclass
class Chainring(Component):
    tooth_number: int
    offset: int


@dataclass
class Cassette(Component):
    speeds: int
    tooth_range: str  # might be divided into low and high with int values


@dataclass
class Derailleur(Component):
    speeds: int


@dataclass
class Chain(Component):
    speeds_compatibility: int


@dataclass
class Saddle(Component):
    pass


@dataclass
class Seatpost(Component):
    telescopic: bool
    diameter: float
    travel: int


@dataclass
class BikeComponents:
    frame: Frame
    shock: Shock
    fork: Fork
    handlebars: Handlebars
    stem: Stem
    headset: Headset
    grips: Grips
    front_break: Break
    rear_break: Break
    front_wheel: Wheel
    rear_wheel: Wheel
    bottom_bracket: BottomBracket
    cranks: Cranks
    pedals: Pedals
    chainring: Chainring
    cassette: Cassette
    derailleur: Derailleur
    chain: Chain
    saddle: Saddle
    seatpost: Seatpost


class PressureUnits(Enum):
    PSI = "psi"
    BAR = "bar"


@dataclass
class Pressure:
    value: int
    units: PressureUnits


@dataclass
class SuspensionSetup:
    pressure: Pressure
    fast_compression: int
    low_compression: int
    fast_rebound: int
    low_rebound: int


@dataclass
class BikeSetup:
    front_tyre: Pressure
    rear_tyre: Pressure
    fork: SuspensionSetup
    shock: SuspensionSetup
    stem_height: int
    saddle_height: int
    brake_levers_angle: int
    chain_length: int
    chainline: int


@dataclass
class Bike:
    name: str
    purchase_date: datetime.time
    total_usage: Usage
    initial_value = {int, str}  # {value, currency}
    geometry: Geometry
    components: BikeComponents
    setup: BikeSetup
