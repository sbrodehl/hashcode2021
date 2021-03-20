import logging

from .basesolver import BaseSolver
from .schedule import Schedule

LOGGER = logging.getLogger(__name__)


class Heuristics(BaseSolver):
    """Solve the problem nice and steady!
    """
    def __init__(self, input_str):
        super().__init__(input_str)

    def solve(self):
        """Compute a solution to the given problem.

        Save everything in an internal state.

        :return: True, if a solution is found, False otherwise
        """
        self.solution = []
        (d, f), streets, cars, intersections = self.data
        # naive thing: intersections with only one in can be 'green' all the time
        for intersection in intersections:
            if len(intersection.incoming) == 1:
                # always on!
                intersection.schedule = Schedule(
                    intersection.id,
                    intersection.incoming,
                    [(1, name) for name in intersection.incoming]
                )
                self.solution.append(intersection.schedule)

        LOGGER.info(f"{len(self.solution)} / {len(intersections)}"
                    f" ({len(self.solution) * 100.0 / len(intersections):.2f}%) intersections are useless.")

        # add heuristic for streets regarding visits
        for car in cars:
            for street in car.streets:  # TODO: revisit this
                streets[street].visits += 1
            streets[car.streets[0]].starting_cars += 1
        empty_streets = 0
        for street in streets:
            if streets[street].visits == 0:
                empty_streets += 1
        LOGGER.info(f"{empty_streets} / {len(streets)}"
                    f" ({empty_streets * 100.0 / len(streets):.2f}%) streets are not used.")

        # add schedule based and (overall) car frequency
        for intersection in intersections:
            # skip intersections with schedules
            if intersection.schedule is not None:
                continue
            visits = {name: streets[name].visits for name in intersection.incoming if streets[name].visits > 0}
            duration = {k: int(d * v / sum(visits.values())) for k, v in visits.items()}
            duration = {k: int(v / min(duration.values())) for k, v in duration.items()}
            duration = dict(sorted(duration.items(), key=lambda item: item[1] * streets[item[0]].starting_cars, reverse=True))
            # daily commute special / kaggle
            # duration = dict(sorted({name: 1 for name in intersection.incoming if streets[name].visits > 0}.items(), key=lambda item: streets[item[0]].starting_cars, reverse=True))
            if len(duration) > 0:
                intersection.schedule = Schedule(
                    intersection.id,
                    list(duration.keys()),
                    [(duration[name], name) for name in duration]
                )
                self.solution.append(intersection.schedule)
            else:
                LOGGER.debug(f"No schedule, no incoming traffic at {intersection}.")
        return True
