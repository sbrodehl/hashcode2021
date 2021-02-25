import logging
import collections

from .pizza import Pizza
from .delivery import Delivery

LOGGER = logging.getLogger(__name__)


def parse_input(file_in):
    """
    Parse input file
    :param file_in: input file name
    :return: (m, t2, t3, t4), available_pizzas
    """
    LOGGER.debug("Parsing file '{}'".format(file_in))
    available_pizzas = []
    with open(file_in, 'r') as f:
        first_line = f.readline().strip()
        l_ = list(map(int, list(first_line.split(" "))))
        m = l_[0]  # (1 ≤ M ≤ 100.000) - the number of pizzas available in the pizzeria
        t2 = l_[1]  # (0 ≤ T2 ≤ 50.000) - the number of 2-person teams
        t3 = l_[2]  # (0 ≤ T3 ≤ 50.000) - the number of 3-person teams
        t4 = l_[3]  # (0 ≤ T4 ≤ 50.000) - the number of 4-person teams

        for pid, line in enumerate(f.readlines()):
            _split = line.strip().split(' ')
            ingredients = set(_split[1:])  # (1 ≤ I ≤ 10.000) - the number of ingredients
            assert len(ingredients) == int(_split[0])
            available_pizzas.append(Pizza(pid, ingredients))

        assert pid + 1 == m

    LOGGER.debug("Parsing '{}' - Done!".format(file_in))
    return m, collections.OrderedDict({4: t4, 3: t3, 2: t2}), available_pizzas


def parse_output(file_out, problem_set):
    """
    Parse output file
    :param file_out: output file name (solution)
    :param problem_set: input problem set
    :return: n, deliveries
    """
    LOGGER.debug("Parsing '{}'".format(file_out))
    solution = []
    with open(file_out, 'r') as f:
        first_line = f.readline().strip()
        deliveries = int(first_line)

        did = -1
        for did, line in enumerate(f.readlines()):
            l_ = list(map(int, line.strip().split(' ')))
            solution.append(Delivery(int(l_[0]), set(map(int, l_[1:])), pizzas=problem_set[2]))

        # check read amount of deliveries
        assert did + 1 == deliveries

    LOGGER.debug("Parsing '{}' - Done!".format(file_out))
    return solution


def write_output(file_out, solution):
    LOGGER.debug("Writing solution '{}'".format(file_out))
    with open(file_out, 'w') as f:
        f.write("{}\n".format(str(len(solution))))
        for delivery in solution:
            f.write(f"{delivery.team_size} {' '.join(list(map(str, delivery.pizza_ids)))}\n")
