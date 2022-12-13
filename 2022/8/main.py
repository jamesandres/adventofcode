import sys
import re
from collections import namedtuple
from ipdb import launch_ipdb_on_exception
from copy import deepcopy


def main(grid):
    """
    --- Day 8: Treetop Tree House ---

    The expedition comes across a peculiar patch of tall trees all planted carefully in a grid. The
    Elves explain that a previous expedition planted these trees as a reforestation effort. Now,
    they're curious if this would be a good location for a tree house.

    First, determine whether there is enough tree cover here to keep a tree house hidden. To do
    this, you need to count the number of trees that are visible from outside the grid when looking
    directly along a row or column.

    The Elves have already launched a quadcopter to generate a map with the height of each tree
    (your puzzle input). For example:

    30373
    25512
    65332
    33549
    35390

    Each tree is represented as a single digit whose value is its height, where 0 is the shortest
    and 9 is the tallest.

    A tree is visible if all of the other trees between it and an edge of the grid are shorter than
    it. Only consider trees in the same row or column; that is, only look up, down, left, or right
    from any given tree.

    All of the trees around the edge of the grid are visible - since they are already on the edge,
    there are no trees to block the view. In this example, that only leaves the interior nine trees
    to consider:

      - The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom
        since other trees of height 5 are in the way.)
      - The top-middle 5 is visible from the top and right.
      - The top-right 1 is not visible from any direction; for it to be visible, there would need to
        only be trees of height 0 between it and an edge.
      - The left-middle 5 is visible, but only from the right.
      - The center 3 is not visible from any direction; for it to be visible, there would need to be
        only trees of at most height 2 between it and an edge.
      - The right-middle 3 is visible from the right.
      - In the bottom row, the middle 5 is visible, but the 3 and 4 are not.

    With 16 trees visible on the edge and another 5 visible in the interior, a total of 21 trees are
    visible in this arrangement.

    Consider your map; how many trees are visible from outside the grid?
    """
    print(num_visible(grid))


def main2(commands):
    pass


def num_visible(grid):
    width = len(grid[0])
    height = len(grid)
    num = 0
    seen = deepcopy(grid)
    # walk a diagonal
    for i in range(0, width):
        print(f'DIAG {i},{i}')
        max_x = -1
        for x in range(0, i + 1):
            print(f'  A: {x},{i} ({grid[x][i]} >? {max_x})')
            if grid[x][i] > max_x and seen[x][i] != '@':
                print(f'    SEEN {x},{i} going {{0 -> {i}}}, {grid[x][i]}>{max_x}')
                seen[x][i] = '@'
                num += 1
                max_x = grid[x][i]
        max_x = -1
        for x in range(width - 1, i - 1, -1):
            print(f'  B: {x},{i} ({grid[x][i]} >? {max_x})')
            if grid[x][i] > max_x and seen[x][i] != '@':
                print(f'    SEEN {x},{i} going {{{width-1} -> {i}}}, {grid[x][i]}<{max_x}')
                seen[x][i] = '@'
                num += 1
                max_x = grid[x][i]
        max_y = -1
        for y in range(0, i + 1):
            print(f'  C: {i},{y} ({grid[i][y]} >? {max_y})')
            if grid[i][y] > max_y and seen[i][y] != '@':
                print(f'    SEEN {i},{y} going {{0 -> {i}}}, {grid[i][y]}>{max_y}')
                seen[i][y] = '@'
                num += 1
                max_y = grid[i][y]
        max_y = -1
        for y in range(height - 1, i - 1, -1):
            print(f'  D: {i},{y} ({grid[i][y]} > {max_y})')
            if grid[i][y] > max_y and seen[i][y] != '@':
                print(f'    SEEN {i},{y} going {{{height-1} -> {i}}}, {grid[i][y]}<{max_y}')
                seen[i][y] = '@'
                num += 1
                max_y = grid[i][y]
    print('\n'.join([''.join(map(str, row)) for row in seen]))
    return num


def parse(input):
    return [[int(raw_tree) for raw_tree in line] for line in input.split('\n')]


def raw_input(filename):
    return open(filename, "r").read().rstrip("\n")


if __name__ == "__main__":
    with launch_ipdb_on_exception():
        filename = sys.argv[1]
        if len(sys.argv) > 2 and sys.argv[2] == "2":
            main2(parse(raw_input(filename)))
        else:
            main(parse(raw_input(filename)))
