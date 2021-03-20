from collections import deque
from typing import Union
from dataclasses import dataclass

from .street import Street


@dataclass
class Car:
    """Class representing a car with its path."""
    id: int
    streets: deque[Union[Street, str]]
    travel_time: int = 0

    def is_complete(self) -> bool:
        return len(self.streets) == 0
