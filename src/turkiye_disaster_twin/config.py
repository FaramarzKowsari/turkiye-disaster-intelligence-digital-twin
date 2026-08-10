from dataclasses import dataclass


@dataclass(frozen=True)
class IstanbulBounds:
    min_lat: float = 40.75
    max_lat: float = 41.35
    min_lon: float = 27.95
    max_lon: float = 29.65


ISTANBUL_BOUNDS = IstanbulBounds()
