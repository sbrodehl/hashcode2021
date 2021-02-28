from typing import Union
from dataclasses import dataclass


@dataclass
class Street:
    """Class representing a street with intersections and travel time."""
    id: int
    begin_intersection: Union[int, "Intersection"]
    end_intersection: Union[int, "Intersection"]
    name: str
    travel_time: int
    visits: int = 0
    starting_cars: int = 0
