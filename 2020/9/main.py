import sys
import re
import functools
from itertools import combinations
from copy import deepcopy

from kitchen_sink import u


def load(filename):
    return parse(u(open(filename, 'rb').read()[:-1]))


def parse(input_text):
    return [int(n) for n in input_text.split('\n')]


def check(numbers, preamble_len):
    previous = numbers[:preamble_len]
    for number in numbers[preamble_len:]:
        if not any(sum(combo) == number for combo in combinations(previous, r=2)):
            return number
        previous.pop(0)
        previous.append(number)
    return True


def contiguous_sum(numbers, target):
    window = []
    for number in numbers:
        while sum(window) > target:
            window.pop(0)
        if len(window) > 1 and sum(window) == target:
            return window
        window.append(number)
    return False



TEST_INPUT = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""
def test():
    numbers = parse(TEST_INPUT)
    assert check(numbers, 5) == 127 
    assert contiguous_sum(numbers, 127) == [15, 25, 47, 40] 
    print('PASS')

