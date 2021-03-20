from typing import List, Dict

from .street import Street
from .car import Car
from .intersection import Intersection
from .schedule import Schedule


class Simulation:

    def __init__(self, duration: int, streets: Dict[str, Street], cars: List[Car], intersections: List[Intersection]):
        self.duration = duration
        self.step: int = -1
        self.streets: Dict[str, Street] = streets
        self.cars: List[Car] = cars
        self.intersections: List[Intersection] = intersections
        self.schedules: List[Schedule] = []

    def setup(self, schedules):
        self.schedules = schedules
        # initialize intersection with schedules
        for s in self.schedules:
            self.intersections[s.intersection_id].schedule = s
        # place cars in their start waiting lists
        for c in self.cars:
            s_name = c.streets.popleft()
            self.streets[s_name].waiting.append(c)
            c.waiting = True
            c.waiting_at = s_name
        return self

    def run(self, duration: int = None):
        duration = duration if duration is not None else self.duration
        for t in range(duration):
            self.step += 1
            self.tick()
        return self

    def tick(self):
        # update lights per intersection
        for i in self.intersections:
            if i.schedule is not None:
                i.schedule.tick()

        # move cars over intersection
        for i in self.intersections:
            # continue, if no schedule available
            if i.schedule is None:
                continue
            # check if vehicles are waiting
            w = self.streets[i.schedule.green].waiting
            if len(w) == 0:
                continue
            v = w.popleft()  # first vehicle waiting
            s = v.streets.popleft()  # next street in path of vehicle
            s = self.streets[s]  # id -> object
            s.driving[v.id] = s.travel_time
            v.waiting_at = None
            v.waiting = False

        # move cars one step ahead
        for sid in self.streets:
            s = self.streets[sid]
            # update travel time of vehicles
            for v in list(s.driving.keys()):
                tt = s.driving[v] - 1
                # check if this changes status of vehicle
                if tt < 0:
                    raise RuntimeError("Travel time of a vehicle can't be negative!")
                if tt == 0:
                    # reached end of the street, either
                    #  - place vehicle in the waiting line for the intersection
                    #  - remove vehicle, since it reached destination
                    v = self.cars[v]  # id -> object
                    del s.driving[v.id]  # remove from street
                    if v.is_complete():
                        # reached end of route
                        v.travel_time = self.step + 1
                    else:
                        # place at intersection
                        s.waiting.append(v)
                        v.waiting = True
                        v.waiting_at = s.name
                else:  # nothing happens
                    s.driving[v] = tt
