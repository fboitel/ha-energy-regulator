from dataclasses import dataclass, field
from .const import BATTERIES

@dataclass
class Store:
    automatic_mode: bool = True
    manual_power: float = 0
    shelly_power: float = 0
    battery_powers: dict[str, float] = field(
        default_factory=lambda: dict.fromkeys(BATTERIES, 0.0)
    )
    active_batteries: list[str] = field(
        default_factory=lambda: [key for key in BATTERIES]
    )