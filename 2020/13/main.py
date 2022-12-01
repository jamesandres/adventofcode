import sys
import re
import functools
from itertools import combinations
from copy import deepcopy

from kitchen_sink import u


def load(filename):
    return parse(u(open(filename, 'rb').read()[:-1]))


def parse(input_text):
    arrival, busses = input_text.split('\n')
    busses = [int(num) if num != 'x' else None
              for num in busses.split(',')]
    return int(arrival), busses


def earliest_bus(arrival, busses):
    return sorted(next_arrivals(arrival, busses))[0]


def next_arrivals(arrival, busses):
    for num in busses:
        if num is None:
            continue
        next_arrival = arrival // num * num
        if next_arrival < arrival:
            next_arrival += num
        yield next_arrival, num


def earliest_rhythm_bruteforce(busses, t=0):
    def make_matcher(i, num):
        def closure(t):
            if t % 1000000 == 0:
                print(f'({t} + {i}) % {num} -> {(t + i) % num}')
            return (t + i) % num == 0
        return closure
    matchers = [make_matcher(i, num)
                for i, num in enumerate(busses)
                if num is not None]
    while True:
        if all(fn(t) for fn in matchers):
            return t
        t += 1


def earliest_rhythm_crt(busses):
    from sympy.ntheory.modular import crt
    moduli_remainders = [(num, i,) for i, num in enumerate(busses)
                         if num is not None]
    moduli, remainders = unzip(moduli_remainders)
    result = crt(moduli, remainders)
    return result[1] % result[0]


def unzip(a_list_of_tuples):
    return list(zip(*a_list_of_tuples))


TEST_INPUT = """939
7,13,x,x,59,x,31,19"""
def test():
    arrival, busses = parse(TEST_INPUT)
    assert earliest_bus(arrival, busses) == (944, 59)
    assert earliest_rhythm_crt(busses) == 1068781
    print('PASS')

