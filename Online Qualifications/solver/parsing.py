import logging

from .street import Street
from .car import Car
from .intersection import Intersection
from .schedule import Schedule


LOGGER = logging.getLogger(__name__)


def parse_input(file_in):
    """
    Parse input file
    :param file_in: input file name
    :return: (duration, bonus), streets, cars, intersections
    """
    LOGGER.info("Parsing file '{}'".format(file_in))
    streets = {}
    cars = []
    intersections = None
    with open(file_in, 'r') as fp:
        # read META data
        d, i, s, v, f = list(map(int, list(fp.readline().strip().split(" "))))
        intersections = [Intersection(idx) for idx in range(i)]

        # read all STREETS
        for street_id in range(s):
            l_ = fp.readline().strip().split(' ')
            b, e = list(map(int, l_[:2]))
            name, l = l_[2], int(l_[3])
            streets[name] = Street(street_id, b, e, name, l)
            intersections[b].add_outgoing(streets[name])
            intersections[e].add_incoming(streets[name])

        assert len(streets) == s

        # read all CARS
        for car_id in range(v):
            l_ = fp.readline().strip().split(' ')
            p = int(l_[0])
            names = l_[1:]
            assert p == len(names)
            cars.append(Car(car_id, names))
            starting_street = names[0]
            streets[starting_street].starting_cars += 1

        assert len(cars) == v

    LOGGER.info(f"Data set with duration {d}, intersections {i}, streets {s}, cars {v} and bonus points {f}.")
    LOGGER.info(f"Read {len(cars)} cars and {len(streets)} streets.")
    LOGGER.info("Parsing '{}' - Done!".format(file_in))
    return (d, f), streets, cars, intersections


def parse_output(file_out):
    """
    Parse output file
    :param file_out: output file name (solution)
    :return: schedules
    """
    LOGGER.info("Parsing '{}'".format(file_out))
    solution = []
    with open(file_out, 'r') as f:
        intersections = int(f.readline().strip())

        for idx in range(intersections):
            intersection_id = int(f.readline().strip())
            incoming_streets = int(f.readline().strip())
            order = []
            covered_streets = []
            for street_idx in range(incoming_streets):
                street_name, duration = f.readline().strip().split()
                order.append((int(duration), street_name))
                covered_streets.append(street_name)
            solution.append(Schedule(intersection_id, covered_streets, order))

    LOGGER.info("Parsing '{}' - Done!".format(file_out))
    return solution


def write_output(file_out, solution: list[Schedule]):
    LOGGER.debug("Writing solution '{}'".format(file_out))
    with open(file_out, 'w') as f:
        f.write("{}\n".format(str(len(solution))))
        for s in solution:
            f.write(f"{s.intersection_id}\n")
            f.write(f"{len(s.streets_covered)}\n")
            for sec, street_name in s.order:
                f.write(f"{street_name} {sec}\n")
    LOGGER.debug("Writing solution '{}' - Done!".format(file_out))
