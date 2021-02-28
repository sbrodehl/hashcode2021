from collections import deque
from typing import Union
from dataclasses import dataclass

from .street import Street
from .intersection import Intersection


@dataclass
class Car:
    """Class representing a car with its path."""
    id: int
    streets: deque[Union[Street, str]]
    waiting: bool = False
    waiting_at: Intersection = None
    travel_time: int = 0

    def is_complete(self) -> bool:
        return len(self.streets) == 0

    def tick(self) -> bool:
        if self.is_complete():
            return False
        # check if we are waiting, and first in queue
        if self.waiting and self.id == self.waiting_at.waiting[self.streets[0].name][0].id:  # peek
            # first in queue, check for green light
            is_green = self.waiting_at.schedule.green == self.streets[0].name
            if not is_green:
                # stuck waiting here
                return False
            s = self.streets.popleft()
            assert self.waiting_at.id == s.end_intersection.id
            # remove car from transit area
            c = self.waiting_at.waiting[s.name].popleft()
            assert c.id == self.id
            self.waiting = False
            self.waiting_at = None
            self.travel_time = 0
            del c, is_green
        # peek current street
        s = self.streets[0]
        # if not waiting, drive ahead
        self.travel_time += 1
        # maybe end of street is reached, and path is not finished, put into transition area
        if s.travel_time == self.travel_time:
            if len(self.streets) == 1:
                # reached destination
                self.streets.popleft()
                return True
            # wait at the intersection
            i = s.end_intersection
            i.waiting[s.name].append(self)
            self.travel_time = 0
            self.waiting_at = i
            self.waiting = True
        return False
