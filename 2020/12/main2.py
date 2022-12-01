import sys
import re
import math
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


def manhattan_distance(instructions, x=0, y=0, waypoint=(-10, 1)):
    for instr, value in instructions:
        if instr in ('L', 'R',):
            waypoint = turn(waypoint, instr, value)
        elif instr in ('N', 'S', 'E', 'W',):
            waypoint = move(instr, value, waypoint)
        elif instr == 'F':
            x = x + waypoint[0] * value
            y = y + waypoint[1] * value
        else:
            raise Exception(f'Unexpected instruction {instr}')
        print(f'{instr}{value} -> waypoint: {repr(waypoint)}, x: {x}, y: {y}')
    return abs(x), abs(y)


def turn(current_waypoint, direction, degrees):
    x1, y1 = current_waypoint
    direction = 1 if direction == 'R' else -1
    radians = math.radians(degrees * direction)
    x2 = round(x1 * math.cos(radians) - y1 * math.sin(radians))
    y2 = round(y1 * math.cos(radians) + x1 * math.sin(radians))
    return x2, y2


def move(heading, value, waypoint):
    vector = {'E': (-1, 0), 'S': (0, -1), 'W': (1, 0), 'N': (0, 1)}
    dx, dy = vector[heading]
    return waypoint[0] + dx * value, waypoint[1] + dy * value


TEST_INPUT = """F10
N3
F7
R90
F11"""
def test():
    assert turn((-10, 1), 'R', 90) == (-1, -10)
    assert turn((-1, -10), 'R', 90) == (10, -1)
    assert turn((10, -1), 'R', 90) == (1, 10)
    assert turn((1, 10), 'R', 90) == (-10, 1)
    assert turn((-10, 1), 'L', 90) == (1, 10)
    assert turn((-10, 1), 'L', 180) == (10, -1)
    instructions = parse(TEST_INPUT)
    assert sum(manhattan_distance(instructions)) == 286
    print('PASS')

