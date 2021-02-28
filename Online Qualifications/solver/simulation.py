import logging
from collections import deque
from typing import List, Dict

from .street import Street
from .car import Car
from .intersection import Intersection
from .schedule import Schedule


class Simulation:

    def __init__(self, duration: int, streets: Dict[str, Street], cars: List[Car], intersections: List[Intersection]):
        self.duration = duration
        self.step: int = 0
        self.streets: Dict[str, Street] = streets
        self.cars: List[Car] = cars
        self.intersections: List[Intersection] = intersections
        self.schedules: List[Schedule] = []

    def setup(self, schedules):
        self.schedules = schedules
        for i in self.intersections:
            for k in i.incoming:
                i.waiting[k] = deque()
        for s in self.schedules:
            s.green = s.order[0][1] if len(s.order) > 0 else None
            self.intersections[s.intersection_id].schedule = s
        # place cars in their start waiting lists
        for c in self.cars:
            s_name = c.streets[0]  # peek
            s = self.streets[s_name]
            i = self.intersections[s.end_intersection]
            i.waiting[s_name].append(c)
            c.waiting = True
            c.waiting_at = i
            c.streets = deque([self.streets[s] for s in c.streets])
        for s in self.streets.values():
            s.begin_intersection = self.intersections[s.begin_intersection]
            s.end_intersection = self.intersections[s.end_intersection]
        return self

    def run(self, t: int = None):
        t = t if t is not None else self.duration
        for _ in range(1, t + 1):
            self.tick()
        return self

    def tick(self):
        # increment global tick step
        self.step += 1
        # move cars one step ahead
        for v in self.cars:
            if v.is_complete():
                continue
            success = v.tick()
            if success:
                v.travel_time = self.step
        # update lights per intersection
        for i in self.intersections:
            if i.schedule is not None:
                i.schedule.tick()
