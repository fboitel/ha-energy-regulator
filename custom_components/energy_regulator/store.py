from dataclasses import dataclass

@dataclass
class Store:
    automatic_mode: bool = True
    manual_power: float = 0