from dataclasses import dataclass, field
from collections import deque


@dataclass
class Street:
    """Class representing a street with intersections and travel time."""
    id: int
    begin_intersection: int
    end_intersection: int
    name: str
    travel_time: int
    waiting: deque["Car"] = field(default_factory=deque, init=False)
    driving: dict = field(default_factory=dict, init=False)
    visits: int = 0
    starting_cars: int = 0
