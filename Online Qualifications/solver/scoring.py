#!/usr/bin/env python3
import logging
from dataclasses import dataclass, field

from .parsing import parse_input, parse_output
from .simulation import Simulation

LOGGER = logging.getLogger(__name__)


class Markup:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


@dataclass
class Score:
    scores: list = field(default_factory=list)
    bonus: int = 0
    early: int = 0
    total: int = 0
    insights: dict = field(default_factory=dict)

    def add(self, bonus, early):
        self.scores.append(bonus + early)
        self.bonus += bonus
        self.early += early
        self.total += bonus + early

    def print_insights(self):
        nsghs = self.insights
        LOGGER.info(f"Submission: {Markup.BOLD}Scoring & Insights{Markup.END}")
        LOGGER.info(f"Your submission scored {Markup.BOLD}{self.total:,}{Markup.END} points."
                    f" This is the sum of {self.bonus:,} bonus points for cars arriving before the deadline"
                    f" ({nsghs['bonus']:,} points each) and {self.early:,} points for early arrival times.")
        deadline_pct = 100.0 * nsghs['before_deadline'] / nsghs['cars']
        travel_t_m = 1.0 * nsghs['sum_travel_times'] / nsghs['before_deadline']
        LOGGER.info(
            f"{nsghs['before_deadline']:,} of {nsghs['cars']:,} cars arrived before the deadline ({deadline_pct:.2f}%)."
            f" The earliest car arrived at its destination after {nsghs['first_car'].travel_time:,} seconds scoring {nsghs['bonus'] + (nsghs['duration'] - nsghs['first_car'].travel_time):,} points,"
            f" whereas the last car arrived at its destination after {nsghs['last_car'].travel_time:,} seconds scoring {nsghs['bonus'] + (nsghs['duration'] - nsghs['last_car'].travel_time):,} points."
            f" Cars that arrived within the deadline drove for an average of {travel_t_m:.2f} seconds to arrive at their destination.")
        LOGGER.debug(f"First car to reach its destination was {nsghs['first_car']}.")
        LOGGER.debug(f"Last car to reach its destination was {nsghs['last_car']}.")
        avg_cycle_l = 1.0 * nsghs['cycle_length'] / nsghs['cycles']
        avg_phase_l = 1.0 * nsghs['green_phase_sum'] / nsghs['green_phases']
        LOGGER.info(
            f"The schedules for the {nsghs['lights']:,} intersections had an average total cycle length of {avg_cycle_l:.2f} seconds."
            f" A traffic light that turned green was scheduled to stay green for {avg_phase_l:.2f} seconds on average.")


def compute_score(file_in, file_out):
    """
    Compute score (with bonus) of submission
    :param file_in: input file
    :param file_out: output file (solution)
    :return: Score
    """
    # read input and output files
    _in = parse_input(file_in)
    _out = parse_output(file_out)
    bonus = _in[0][1]
    duration = _in[0][0]
    sim = Simulation(duration, *(_in[1:])).setup(_out).run()
    s = Score()
    s.insights['bonus'] = bonus
    s.insights['lights'] = len(sim.intersections)
    s.insights['duration'] = duration
    s.insights['cars'] = len(sim.cars)
    s.insights['before_deadline'] = 0
    s.insights['first_car'] = None
    s.insights['last_car'] = None
    s.insights['sum_travel_times'] = 0
    s.insights['cycle_length'] = 0
    s.insights['cycles'] = 0
    s.insights['green_phases'] = 0
    s.insights['green_phase_sum'] = 0
    for v in sim.cars:
        # add score, if car succeded
        if v.is_complete():
            if s.insights['first_car'] is None or s.insights['first_car'].travel_time > v.travel_time:
                s.insights['first_car'] = v
            if s.insights['last_car'] is None or s.insights['last_car'].travel_time < v.travel_time:
                s.insights['last_car'] = v
            s.insights['before_deadline'] += 1
            s.insights['sum_travel_times'] += v.travel_time
            s.add(bonus, (duration - v.travel_time))
    # add more insights
    for i in sim.intersections:
        if i.schedule is None:
            continue
        c = [c[0] for c in i.schedule.order]
        s.insights['green_phases'] += len(c)
        s.insights['green_phase_sum'] += sum(c)
        s.insights['cycle_length'] += i.schedule.length
        s.insights['cycles'] += 1
    return s


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='print score', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('file_in', type=str, help='input file e.g. a_example.in')
    parser.add_argument('file_out', type=str, help='output file e.g. a_example.out')
    parser.add_argument('--debug', action='store_true', help='set debug level')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    score = compute_score(args.file_in, args.file_out)

    print("Score for {}: {} points".format(args.file_out, score.total))
