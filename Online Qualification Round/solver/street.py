from dataclasses import dataclass


@dataclass
class Street:
    """Class representing a street with intersections and travel time."""
    id: int
    begin_intersection: int
    end_intersection: int
    name: str
    travel_time: int
