import sys
import re
import functools
from itertools import combinations
from copy import deepcopy

from kitchen_sink import u


def load(filename):
    return parse(u(open(filename, 'rb').read()[:-1]))


def parse(input_text):
    return [parse_instruction(i) for i in input_text.split('\n')]


def parse_instruction(i):
    matches = re.findall(r'([NSEWLFR])(\d+)', i)
    return matches[0][0], int(matches[0][1])


def manhattan_distance(instructions, heading='E', x=0, y=0):
    for instr, value in instructions:
        if instr in ('L', 'R',):
            heading = turn(heading, instr, value)
        elif instr in ('N', 'S', 'E', 'W',):
            x, y = move(instr, value, x, y)
        elif instr == 'F':
            x, y = move(heading, value, x, y)
        else:
            raise Exception(f'Unexpected instruction {instr}')
    return abs(x), abs(y)


def turn(current_heading, direction, degrees):
    compass = ['E', 'S', 'W', 'N']
    index = compass.index(current_heading)
    direction = 1 if direction == 'R' else -1
    return compass[(index + (degrees // 90) * direction) % len(compass)]


def move(heading, value, x, y):
    vector = {'E': (0, -1), 'S': (-1, 0), 'W': (0, 1), 'N': (1, 0)}
    dx, dy = vector[heading]
    return x + dx * value, y + dy * value


TEST_INPUT = """F10
N3
F7
R90
F11"""
def test():
    instructions = parse(TEST_INPUT)
    assert turn('E', 'R', 90) == 'S'
    assert sum(manhattan_distance(instructions)) == 25
    print('PASS')

