from dataclasses import dataclass, field

from .street import Street
from .schedule import Schedule


@dataclass
class Intersection:
    """Class representing a street with intersections and travel time."""
    id: int
    incoming: list = field(default_factory=list, init=False)
    outgoing: list = field(default_factory=list, init=False)
    schedule: Schedule = None
    waiting: int = 0

    def add_incoming(self, street: Street):
        if street.name not in self.incoming:
            self.incoming.append(street.name)

    def add_outgoing(self, street: Street):
        if street.name not in self.outgoing:
            self.outgoing.append(street.name)
