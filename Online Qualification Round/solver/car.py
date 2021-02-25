from dataclasses import dataclass


@dataclass
class Car:
    """Class representing a car with its path."""
    id: int
    streets: list
