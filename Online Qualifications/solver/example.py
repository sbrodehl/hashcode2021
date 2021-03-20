import logging

from .basesolver import BaseSolver
from .schedule import Schedule

LOGGER = logging.getLogger(__name__)


class Example(BaseSolver):
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
        # naive thing: intersections with only one in and one out can be 'green' all the time
        (d, i, s, v, f), streets, cars, intersections = self.data
        for intersection in intersections:
            if len(intersection.incoming) == 1:
                # always on!
                self.solution.append(Schedule(
                    intersection.id,
                    [(1, name) for name in intersection.incoming]
                ))
                intersection.has_schedule = True
                # TODO simplify map by joining both streets?
        # add random schedule for other intersections ;-)
        for intersection in intersections:
            # skip intersections with schedules
            if intersection.has_schedule:
                continue
            self.solution.append(Schedule(
                intersection.id,
                [(1, name) for name in intersection.incoming]
            ))
        return True
