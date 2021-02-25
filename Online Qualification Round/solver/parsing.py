import logging

from .street import Street
from .car import Car


LOGGER = logging.getLogger(__name__)


def parse_input(file_in):
    """
    Parse input file
    :param file_in: input file name
    :return: streets, cars
    """
    LOGGER.info("Parsing file '{}'".format(file_in))
    streets = {}
    cars = []
    with open(file_in, 'r') as fp:
        # read META data
        d, i, s, v, f = list(map(int, list( fp.readline().strip().split(" "))))

        # read all STREETS
        for street_id in range(s):
            l_ = fp.readline().strip().split(' ')
            b, e = list(map(int, l_[:2]))
            name, l = l_[2], int(l_[3])
            streets[name] = Street(street_id, b, e, name, l)

        assert len(streets) == s

        # read all CARS
        for car_id in range(v):
            l_ = fp.readline().strip().split(' ')
            p = int(l_[0])
            names = l_[1:]
            assert p == len(names)
            cars.append(Car(car_id, names))

        assert len(cars) == v

    LOGGER.info(f"Read {len(cars)} cars and {len(streets)} streets.")
    LOGGER.info("Parsing '{}' - Done!".format(file_in))
    return streets, cars


def parse_output(file_out, problem_set):
    """
    Parse output file
    :param file_out: output file name (solution)
    :param problem_set: input problem set
    :return: n, deliveries
    """
    LOGGER.info("Parsing '{}'".format(file_out))
    solution = []
    with open(file_out, 'r') as f:
        first_line = f.readline().strip()
        print(first_line)

        lid = -1
        for lid, line in enumerate(f.readlines()):
            l_ = list(map(int, line.strip().split(' ')))

        print(f"Read {lid} additional lines.")

    LOGGER.info("Parsing '{}' - Done!".format(file_out))
    return solution


def write_output(file_out, solution):
    LOGGER.debug("Writing solution '{}'".format(file_out))
    with open(file_out, 'w') as f:
        f.write("{}\n".format(str(len(solution))))
        for s in solution:
            f.write(f"{s}\n")
