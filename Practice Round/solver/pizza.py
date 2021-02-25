from dataclasses import dataclass


@dataclass
class Pizza:
    """Class representing a pizza with ingredients."""
    id: int
    ingredients: set
    delivered: bool = False

    def __len__(self):
        return len(self.ingredients)
