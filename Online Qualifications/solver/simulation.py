from typing import List, Dict, Set
import time
import logging

from .street import Street
from .car import Car
from .intersection import Intersection
from .schedule import Schedule


LOGGER = logging.getLogger(__name__)


class Simulation:

    def __init__(self, duration: int, streets: Dict[str, Street], cars: List[Car], intersections: List[Intersection]):
        self.duration = duration
        self.step: int = -1
        self.streets: Dict[str, Street] = streets
        self.cars: List[Car] = cars
        self.intersections: List[Intersection] = intersections
        self.schedules: List[Schedule] = []
        self._intersections_updates: Set[int] = set()
        self._intersections_updates_check: Set[int] = set()
        self._schedules_updates: Set[int] = set()
        self._streets_updates: Set[str] = set()
        self._streets_updates_removal: Set[str] = set()
        self._timer = time.CLOCK_THREAD_CPUTIME_ID

    def setup(self, schedules):
        self.schedules = schedules
        # initialize intersection with schedules
        for s in self.schedules:
            self.intersections[s.intersection_id].schedule = s
        # place cars in their start waiting lists
        for c in self.cars:
            s_name = c.streets.popleft()
            self.streets[s_name].waiting.append(c)
            self.intersections[self.streets[s_name].end_intersection].waiting += 1
            c.waiting = True
            c.waiting_at = s_name
            # gather statistics
            self.streets[s_name].starting_cars += 1
            for s_name in c.streets:
                self.streets[s_name].visits += 1
        # remove useless intersections and unused streets from simulation
        # keep track of active vehicles / streets / intersections
        self._schedules_updates = set(
            i.id
            for i in self.intersections
            if i.schedule is not None and len(i.schedule.order) > 1
        )
        self._intersections_updates = set(
            i.id
            for i in self.intersections
            if any(self.streets[s].starting_cars > 0 for s in i.incoming) and i.schedule is not None
        )
        self._streets_updates = set(
            sid
            for sid, s in self.streets.items()
            if len(s.driving) > 0
        )
        return self

    def run(self, duration: int = None):
        duration = duration if duration is not None else self.duration
        start = time.clock_gettime(self._timer)
        # set 'static' intersections
        for iidx in set(s.intersection_id for s in self.schedules).difference(self._schedules_updates):
            self.intersections[iidx].schedule.tick()

        # run steps of the simulation
        for t in range(duration):
            self.step += 1
            self.tick()

        LOGGER.info(
            f"{self.__class__.__name__}::run "
            f"{time.clock_gettime(self._timer) - start:.5f}s"
        )
        return self

    def tick(self):
        self.update_schedules()
        self.update_intersections()
        self.update_streets()
        # check loop updates
        self._intersections_updates.difference_update(set(i for i in self._intersections_updates_check if self.intersections[i].waiting == 0))
        self._intersections_updates.update(set(i for i in self._intersections_updates_check if self.intersections[i].waiting != 0))
        self._streets_updates.difference_update(self._streets_updates_removal)
        self._intersections_updates_check.clear()
        self._streets_updates_removal.clear()

    def update_schedules(self):
        # update lights per intersection
        for iidx in self._schedules_updates:
            self.update_schedule(iidx)

    def update_schedule(self, iidx):
        i = self.intersections[iidx]
        if i.schedule is not None:
            i.schedule.tick()

    def update_intersections(self):
        # move cars over intersection
        for iidx in self._intersections_updates:
            self.update_intersection(iidx)

    def update_intersection(self, iidx):
        try:  # check if vehicle is waiting
            v = self.streets[self.intersections[iidx].schedule.green].waiting.popleft()
        except IndexError:
            return
        self.intersections[iidx].waiting -= 1
        if self.intersections[iidx].waiting == 0:
            self._intersections_updates_check.add(iidx)
        s = v.streets.popleft()  # next street in path of vehicle
        s = self.streets[s]  # id -> object
        s.driving[v.id] = s.travel_time
        self._streets_updates.add(s.name)
        v.waiting_at = None
        v.waiting = False

    def update_streets(self):
        # move cars one step ahead
        for s in self._streets_updates:
            self.update_street(s)

    def update_street(self, s):
        s = self.streets[s]  # id -> object
        del_v = []
        # update travel time of vehicles
        for v in s.driving:
            tt = s.driving[v] - 1
            # check if this changes status of vehicle
            if tt < 0:
                raise RuntimeError("Travel time of a vehicle can't be negative!")
            if tt == 0:
                # reached end of the street, either
                #  - place vehicle in the waiting line for the intersection
                #  - remove vehicle, since it reached destination
                v = self.cars[v]  # id -> object
                del_v.append(v.id)  # mark for removal
                if v.is_complete():
                    # reached end of route
                    v.travel_time = self.step + 1
                else:
                    # place at intersection
                    s.waiting.append(v)
                    v.waiting = True
                    v.waiting_at = s.name
                    self._intersections_updates.add(s.end_intersection)
                    if self.intersections[s.end_intersection].waiting == 0:
                        self._intersections_updates_check.add(s.end_intersection)
                    self.intersections[s.end_intersection].waiting += 1
            else:  # nothing happens
                s.driving[v] = tt

        # remove from street
        for v in del_v:
            s.driving.pop(v, None)
        # mark for removal from loop
        if len(s.driving) == 0:
            self._streets_updates_removal.add(s.name)
