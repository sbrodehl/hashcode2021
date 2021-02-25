import logging
import collections


LOGGER = logging.getLogger(__name__)


def parse_input(file_in):
    """
    Parse input file
    :param file_in: input file name
    :return: (m, t2, t3, t4), available_pizzas
    """
    LOGGER.info("Parsing file '{}'".format(file_in))
    data = []
    with open(file_in, 'r') as f:
        first_line = f.readline().strip()
        l_ = list(map(int, list(first_line.split(" "))))
        print(first_line)

        lid = -1
        for lid, line in enumerate(f.readlines()):
            l_ = line.strip().split(' ')

        print(f"Read {lid} additional lines.")

    LOGGER.info("Parsing '{}' - Done!".format(file_in))
    return data


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
