import sys
import re
import functools
import itertools
from collections import defaultdict, Counter
from copy import deepcopy

from kitchen_sink import u


def load(filename):
    return parse(u(open(filename, 'rb').read()[:-1]))


def parse(input_text):
    return [int(n) for n in input_text.split('\n')]


TEST_INPUT = """"""
def test():
    data = parse(TEST_INPUT)
    assert data != data
    print('PASS')

