import sys
import re
import functools
import itertools
from copy import deepcopy
from collections import defaultdict

from kitchen_sink import u


def numbers_spoken(numbers, stop_at):
    last_spoken = defaultdict(lambda: 0)
    while len(numbers) < stop_at:
        prev_num = numbers[-1]
        length = len(numbers)
        prev_num_index = length - 2
        if prev_num not in numbers[:-1]:
            distance = 0
        else:
            distance = 0
            for rev_i, prev_prev_num in enumerate(reversed(numbers[:-1])):
                i = length - 3 - rev_i
                if prev_prev_num == prev_num:
                    distance = prev_num_index - i
                    break
        numbers.append(distance)
        numbers_set.add(distance)
    return numbers


# N : 0, 3, 6, x?
# p1:          (undefined)
# p2:       ^
# N : 0, 3, 6, 0, x?
# p1: ^
# p2:          ^
# N : 0, 3, 6, 0, 4, x?
# p1:                (undefined)
# p2:             ^
def numbers_spoken2(numbers, stop_at):
    prev_index = {n: i for i, n in enumerate(numbers)}
    while len(numbers) < stop_at:
        current = numbers[-1]
        current_i = len(numbers) - 1
        if current_i % 1000000 == 0:
            print(f'.. {current_i}/{stop_at}')
        if current not in prev_index:
            numbers.append(0)
        else:
            numbers.append(current_i - prev_index[current])
        prev_index[current] = current_i
    return numbers


TEST_INPUT = """"""
def test():
    assert numbers_spoken2([0,3,6], 10) == [0, 3, 6, 0, 3, 3, 1, 0, 4, 0]
    assert numbers_spoken2([1,3,2], 2020)[-1] == 1
    assert numbers_spoken2([2,1,3], 2020)[-1] == 10
    assert numbers_spoken2([1,2,3], 2020)[-1] == 27
    assert numbers_spoken2([2,3,1], 2020)[-1] == 78
    assert numbers_spoken2([3,2,1], 2020)[-1] == 438
    assert numbers_spoken2([3,1,2], 2020)[-1] == 1836
    print('PASS')

