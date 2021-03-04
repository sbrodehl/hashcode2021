from dataclasses import dataclass, field


@dataclass
class Schedule:
    """Class representing a street with intersections and travel time."""
    intersection_id: int
    streets_covered: list
    order: list
    step: int = 0
    green: str = None
    length: int = field(init=False, default=0)
    green_lut: list = field(init=False, default=None)

    def __post_init__(self):
        self.length = 0
        self.green_lut = []
        for l, s in self.order:
            self.length += l
            self.green_lut.extend([s] * l)

    def tick(self):
        # advance schedule tick
        self.step = self.step % self.length
        # set green light
        self.green = self.green_lut[self.step]
        self.step += 1
