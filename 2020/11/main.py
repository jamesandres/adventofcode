import sys
import re
import functools
from itertools import combinations
from copy import deepcopy

from kitchen_sink import u


def load(filename):
    return parse(u(open(filename, 'rb').read()[:-1]))


def parse(input_text):
    return [list(line) for line in input_text.split('\n')]


def count_occupied_seats(grid):
    counter = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '#':
                counter += 1
    return counter


def run_until_stable(grid, iterator, limit):
    next_grid = None
    while True:
        next_grid = iterate(grid, iterator, limit)
        if grepr(next_grid) == grepr(grid):
            break
        grid = next_grid
    return next_grid


def iterate(grid, iterator, limit):
    next_grid = deepcopy(grid)
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '.':
                continue
            elif grid[y][x] == 'L' and empty_enough(grid, x, y, iterator):
                next_grid[y][x] = '#'
            elif grid[y][x] == '#' and too_crowded(grid, x, y, iterator, limit):
                next_grid[y][x] = 'L'
    gprint(next_grid)
    print()
    return next_grid



def empty_enough(grid, x, y, iterator):
    for x2, y2 in iterator(grid, x, y):
        if get(grid, x2, y2) == '#':
            return False
    return True


def too_crowded(grid, x, y, iterator, limit):
    num_occupied = 0
    for x2, y2 in iterator(grid, x, y):
        if get(grid, x2, y2) == '#':
            num_occupied += 1
        #print(x2, y2, get(grid, x2, y2), num_occupied)
        if num_occupied >= limit:
            return True
    return False


def around(grid, x, y):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            x2 = x + i
            y2 = y + j
            if get(grid, x2, y2) != None:
                yield x2, y2


def visible(grid, x, y):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            see, x2, y2 = ray(grid, x, y, dx, dy)
            if see in ('#', 'L') and get(grid, x2, y2) != None:
                yield x2, y2


def ray(grid, x, y, dx, dy):
    while True:
        x += dx
        y += dy
        see = get(grid, x, y)
        if see != '.':
            return see, x, y


def get(grid, x, y):
    if  0 <= y < len(grid) and 0 <= x < len(grid[0]):
        return grid[y][x]
    else:
        return None


def gprint(grid):
    print(grepr(grid))


def grepr(grid):
    return '\n'.join([''.join(line) for line in grid])


TEST_INPUT = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""
def test():
    grid = parse(TEST_INPUT)
    assert grepr(run_until_stable(grid, iterator=around, limit=4)) == """#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##"""
    print('PASS')


def test2():
    grid = parse(TEST_INPUT)
    assert grepr(run_until_stable(grid, iterator=visible, limit=5)) == """#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#"""
    print('PASS')

