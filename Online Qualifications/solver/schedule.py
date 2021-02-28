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
    partials: list = field(init=False, default=list)

    def __post_init__(self):
        self.length = sum([l for l, s in self.order])
        total = 0
        self.partials = [total := total + v for v, s in self.order]

    def tick(self):
        # advance schedule tick
        self.step = (self.step + 1) % self.length
        # set green light
        # if only one street is covered
        if len(self.streets_covered) == 1:
            idx = 0
        else:
            idx = next(iter(idx for idx, p in enumerate(self.partials) if p > self.step))
        self.green = self.order[idx][1]
