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

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            # R->L
            highest = -1
            print('R->L ' * 10)
            for i in range(0, y + 1):
                if grid[x][i] > highest and '\33' not in str(seen[x][i]):
                    seen[x][i] = '\33[42m' + str(seen[x][i]) + '\33[0m'
                    debug(x, y, seen, grid)
                    num += 1
                    highest = grid[x][i]
            # R<-L
            highest = -1
            print('R<-L ' * 10)
            for i in range(width - 1, y - 1, -1):
                if grid[x][i] > highest and '\33' not in str(seen[x][i]):
                    seen[x][i] = '\33[42m' + str(seen[x][i]) + '\33[0m'
                    debug(x, y, seen, grid)
                    num += 1
                    highest = grid[x][i]
            # U->D
            highest = -1
            print('U->D ' * 10)
            for i in range(0, x + 1):
                if grid[i][y] > highest and '\33' not in str(seen[i][y]):
                    seen[i][y] = '\33[42m' + str(seen[i][y]) + '\33[0m'
                    debug(x, y, seen, grid)
                    num += 1
                    highest = grid[i][y]
            # U<-D
            highest = -1
            print('U<-D ' * 10)
            for i in range(height - 1, x + 1, -1):
                if grid[i][y] > highest and '\33' not in str(seen[i][y]):
                    seen[i][y] = '\33[42m' + str(seen[i][y]) + '\33[0m'
                    debug(x, y, seen, grid)
                    num += 1
                    highest = grid[i][y]
    return num


def main2(grid):
    """
    --- Part Two ---

    Content with the amount of tree cover available, the Elves just need to know the best spot to
    build their tree house: they would like to be able to see a lot of trees.

    To measure the viewing distance from a given tree, look up, down, left, and right from that
    tree; stop if you reach an edge or at the first tree that is the same height or taller than the
    tree under consideration. (If a tree is right on the edge, at least one of its viewing
    distances will be zero.)

    The Elves don't care about distant trees taller than those found by the rules above; the
    proposed tree house has large eaves to keep it dry, so they wouldn't be able to see higher than
    the tree house anyway.

    In the example above, consider the middle 5 in the second row:

    30373
    25512
    65332
    33549
    35390

      - Looking up, its view is not blocked; it can see 1 tree (of height 3).
      - Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right
        next to it).
      - Looking right, its view is not blocked; it can see 2 trees.
      - Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the
        tree of height 5 that blocks its view).

    A tree's scenic score is found by multiplying together its viewing distance in each of the four
    directions. For this tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).

    However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

    30373
    25512
    65332
    33549
    35390

      - Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
      - Looking left, its view is not blocked; it can see 2 trees.
      - Looking down, its view is also not blocked; it can see 1 tree.
      - Looking right, its view is blocked at 2 trees (by a massive tree of height 9).

    This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.

    Consider each tree on your map. What is the highest scenic score possible for any tree?
    """
    print('TODO: Do part 2')


def debug(x, y, seen, grid):
    seen2 = deepcopy(seen)
    seen2[x][y] = '\33[44m' + str(grid[x][y]) + '\33[0m'
    print('\n'.join([''.join(map(str, row)) for row in seen2]))


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
