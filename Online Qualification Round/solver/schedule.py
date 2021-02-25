from dataclasses import dataclass


@dataclass
class Schedule:
    """Class representing a street with intersections and travel time."""
    intersection_id: int
    streets_covered: list
    order: list
