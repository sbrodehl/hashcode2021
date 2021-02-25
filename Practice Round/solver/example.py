import logging

from .basesolver import BaseSolver
from .delivery import Delivery

LOGGER = logging.getLogger(__name__)

class Solver(BaseSolver):
    """Solve the problem nice and steady!
    """
    def __init__(self, input_str):
        super().__init__(input_str)

    def solve(self):
        """Compute a solution to the given problem.

        Save everything in an internal state.

        :return: True, if a solution is found, False otherwise
        """
        m, teams, pizzas = self.data
        # sort pizzas by number of ingredients and add a boolean flag to mark selection
        pizzas.sort(key=len, reverse=True)
        self.solution = []
        for ts, ds in teams.items():
            LOGGER.info(f"Selecting pizzas for teams of {ts}, {ds} deliveries.")
            for d in range(ds):
                delivery = Delivery(ts)
                LOGGER.debug(f"Processing delivery {d + 1}/{ds}.")
                # iterate over amount of needed pizzas for this delivery
                for _ in range(ts):
                    least_overlap = 10001
                    best_pizza = None
                    # iterate over available and unselected pizzas
                    for p in [p for p in pizzas if not p.delivered]:
                        # stop looking for pizzas if enough pizzas are selected
                        if delivery.complete():
                            break
                        elif delivery.empty():
                            # if no pizza is selected, take the first we get
                            delivery.add(p)
                        else:
                            # otherwise, check if we can add a pizza with (completely) new ingredients
                            overlap = len(delivery.ingredients.intersection(p.ingredients))
                            if overlap == 0:
                                delivery.add(p)
                            # if not, take pizza with least overlap
                            else:
                                if overlap < least_overlap:
                                    least_overlap = overlap
                                    best_pizza = p
                    if best_pizza is not None:
                        logging.info(f"Best pizza is {best_pizza} with overlap {least_overlap}.")
                        delivery.add(best_pizza)

                # a valid delivery has enough pizzas for all team members
                if delivery.complete():
                    self.solution.append(delivery)
        return True
