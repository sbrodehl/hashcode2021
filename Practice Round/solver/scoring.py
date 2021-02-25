#!/usr/bin/env python3
import logging
from dataclasses import dataclass, field

import numpy as np

from .parsing import parse_input, parse_output


@dataclass
class Score:
    scores: list = field(default_factory=list)
    total: int = 0

    def add(self, diff_ingredients_sq):
        self.scores.append(diff_ingredients_sq)
        self.total += diff_ingredients_sq * diff_ingredients_sq


def set_log_level(args):
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


def compute_score(file_in, file_out):
    """
    Compute score (with bonus) of submission
    :param file_in: input file
    :param file_out: output file (solution)
    :return: Score
    """
    # read input and output files
    m, teams, pizzas = parse_input(file_in)
    deliveries = parse_output(file_out, (m, teams, pizzas))
    s = Score()
    for d in deliveries:
        # check if all pizzas are available
        if not all(not pizzas[pid].delivered for pid in d.pizza_ids):
            logging.error(f"Delivery contains already delivered pizzas! ({d})")
            break
        # check if enough pizzas are delivery for the team
        if not d.complete():
            logging.error(f"Delivery contains not enough pizzas! ({d})")
            break
        # check amount of deliveries per team size
        if teams[d.team_size] <= 0:
            logging.error(f"More deliveries than teams found for size {d.team_size}!")
            break
        teams[d.team_size] -= 1  # decrease seen deliveries for the team size
        # now compute actual score
        s.add(len(d.ingredients))
    return s


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='print score', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('file_in', type=str, help='input file e.g. a_example.in')
    parser.add_argument('file_out', type=str, help='output file e.g. a_example.out')
    parser.add_argument('--debug', action='store_true', help='set debug level')
    args = parser.parse_args()

    set_log_level(args)

    score = compute_score(args.file_in, args.file_out)

    print("Score for {}: {} points".format(args.file_out, score.total()))
