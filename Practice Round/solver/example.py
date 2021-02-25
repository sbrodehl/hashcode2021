import logging

from .basesolver import BaseSolver
from .delivery import Delivery

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
                    best_improvement = 0
                    next_pizza = None
                    # iterate over available and unselected pizzas
                    for p in [p for p in pizzas if not p.delivered]:
                        # stop looking for pizzas if enough pizzas are selected
                        if delivery.complete():
                            LOGGER.debug("Delivery is COMPLETE.")
                            break
                        # if no pizza is selected, take the first we get
                        if delivery.empty():
                            next_pizza = p
                            best_improvement = len(p)
                            break
                        # since pizzas are ordered, if ingredient length is smaller than current improvement -> skip
                        if len(p) < best_improvement:
                            break
                        # check if we can add a pizza with (completely) new ingredients
                        # or at least select a pizza with the most new ingredients
                        overlap = len(delivery.ingredients.intersection(p.ingredients))
                        improvement = len(p) - overlap

                        _has_improvement = (improvement > best_improvement)
                        _has_equal_improvement = (improvement == best_improvement)
                        _has_lower_overlap = (overlap < least_overlap)
                        if _has_improvement or (_has_equal_improvement and _has_lower_overlap):
                            best_improvement = improvement
                            least_overlap = overlap
                            next_pizza = p
                            # if overlap is zero, no better pizza is available
                            if overlap == 0:
                                break

                    # check if a new pizza is available which improves the score
                    if next_pizza is not None and best_improvement > 0:
                        delivery.add(next_pizza)

                # a valid delivery has enough pizzas for all team members
                if delivery.complete():
                    self.solution.append(delivery)
                else:
                    # free chosen pizzas
                    for pid in delivery.pizza_ids:
                        pizzas[pid].delivered = False
        return True
