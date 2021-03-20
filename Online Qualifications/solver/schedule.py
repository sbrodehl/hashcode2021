from dataclasses import dataclass, field


@dataclass
class Schedule:
    """Class representing a street with intersections and travel time."""
    intersection_id: int
    order: list
    step: int = -1
    green: str = None
    length: int = field(init=False, default=0)
    green_lut: list = field(init=False, default=None)

    def __post_init__(self):
        """Compute schedule duration and green light look-up table."""
        self.length = 0
        self.green_lut = []
        for length, s in self.order:
            self.length += length
            self.green_lut.extend([s] * length)

    def tick(self):
        self.step += 1
        # advance schedule tick
        self.step = self.step % self.length
        # set green light
        self.green = self.green_lut[self.step]
