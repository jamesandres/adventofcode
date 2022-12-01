import sys
import re
import functools
import itertools
from copy import deepcopy
from collections import Counter

from kitchen_sink import u


def load(filename):
    return parse(u(open(filename, 'rb').read()[:-1]))


def parse(input_text):
    return [int(n) for n in input_text.split('\n')]


def distance_counter(numbers):
    distances = [b - a for a, b in pairs(sorted(numbers))]
    return Counter(distances)


def bookends(numbers):
    return [0] + numbers + [numbers[-1] + 3]


def pairs(numbers):
    prev_num = numbers[0]
    for num in numbers[1:]:
        yield prev_num, num
        prev_num = num
        

def bubbles(numbers):
    numbers = sorted(numbers)
    prev_num = 0
    buff = tuple()
    result = []
    for num in numbers:
        if num - prev_num > 1:
            result.append(buff)
            buff = tuple()
        buff = buff + (num,)
        prev_num = num
    if buff:
        result.append(buff)
    return result


def permutations(numbers):
    bubbled_numbers = bubbles(numbers)
    for i, bubble1 in enumerate(bubbled_numbers):
        if len(bubble1) <= 2:
            continue
        for j, bubble2 in enumerate(bubbled_numbers):
            if len(bubble2) <= 2:
                continue
            for bubble1_permute in bubble_permutations(bubble1):
                for bubble2_permute in bubble_permutations(bubble2):
                    bubbled_numbers2 = bubbled_numbers.copy()
                    bubbled_numbers2[i] = bubble1_permute
                    bubbled_numbers2[j] = bubble2_permute
                    yield bubbled_numbers2
            

def bubble_permutations(bubble):
    changable = bubble[1:-1]
    length = len(changable)
    changable = changable + tuple([None] * length)
    for inner in set([p for p in itertools.combinations(changable, r=length)]):
        permutation = (bubble[0],) + tuple([n for n in inner if n]) + (bubble[-1],)
        distances = distance_counter(permutation)
        is_valid = set(distances.keys()).issubset({1, 2, 3})
        if is_valid:
            yield permutation



TEST_INPUT = """16
10
15
5
1
11
7
19
6
12
4"""

TEST_INPUT2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""
def test():
    numbers = parse(TEST_INPUT)
    counter = distance_counter(bookends(sorted(numbers)))
    assert counter[1] == 7
    assert counter[3] == 5
    print('PASS')

