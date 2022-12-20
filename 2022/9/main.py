import sys
import re
from collections import namedtuple
from dataclasses import dataclass
from ipdb import launch_ipdb_on_exception  # type: ignore[import]


def main(commands):
    """
    --- Day 9: Rope Bridge ---

    This rope bridge creaks as you walk along it. You aren't sure how old it is, or whether it can
    even support your weight.

    It seems to support the Elves just fine, though. The bridge spans a gorge which was carved out
    by the massive river far below you.

    You step carefully; as you do, the ropes stretch and twist. You decide to distract yourself by
    modeling rope physics; maybe you can even figure out where not to step.

    Consider a rope with a knot at each end; these knots mark the head and the tail of the rope. If
    the head moves far enough away from the tail, the tail is pulled toward the head.

    Due to nebulous reasoning involving Planck lengths, you should be able to model the positions of
    the knots on a two-dimensional grid. Then, by following a hypothetical series of motions
    (your puzzle input) for the head, you can determine how the tail will move.

    Due to the aforementioned Planck lengths, the rope must be quite short; in fact, the head(H) and
    tail (T) must always be touching (diagonally adjacent and even overlapping both count as
    touching):

    ....
    .TH.
    ....

    ....
    .H..
    ..T.
    ....

    ...
    .H. (H covers T)
    ...

    If the head is ever two steps directly up, down, left, or right from the tail, the tail must
    also move one step in that direction so it remains close enough:

    .....    .....    .....
    .TH.. -> .T.H. -> ..TH.
    .....    .....    .....

    ...    ...    ...
    .T.    .T.    ...
    .H. -> ... -> .T.
    ...    .H.    .H.
    ...    ...    ...

    Otherwise, if the head and tail aren't touching and aren't in the same row or column, the tail
    always moves one step diagonally to keep up:

    .....    .....    .....
    .....    ..H..    ..H..
    ..H.. -> ..... -> ..T..
    .T...    .T...    .....
    .....    .....    .....

    .....    .....    .....
    .....    .....    .....
    ..H.. -> ...H. -> ..TH.
    .T...    .T...    .....
    .....    .....    .....

    You just need to work out where the tail goes as the head follows a series of motions. Assume
    the head and the tail both start at the same position, overlapping.

    For example:

    R 4
    U 4
    L 3
    D 1
    R 4
    D 1
    L 5
    R 2

    This series of motions moves the head right four steps, then up four steps, then left three
    steps, then down one step, and so on. After each step, you'll need to update the position of
    the tail if the step means the head is no longer adjacent to the tail. Visually, these motions
    occur as follows (s marks the starting position as a reference point):

    == Initial State ==

    ......
    ......
    ......
    ......
    H.....  (H covers T, s)

    == R 4 ==

    ......
    ......
    ......
    ......
    TH....  (T covers s)

    ......
    ......
    ......
    ......
    sTH...

    ......
    ......
    ......
    ......
    s.TH..

    ......
    ......
    ......
    ......
    s..TH.

    == U 4 ==

    ......
    ......
    ......
    ....H.
    s..T..

    ......
    ......
    ....H.
    ....T.
    s.....

    ......
    ....H.
    ....T.
    ......
    s.....

    ....H.
    ....T.
    ......
    ......
    s.....

    == L 3 ==

    ...H..
    ....T.
    ......
    ......
    s.....

    ..HT..
    ......
    ......
    ......
    s.....

    .HT...
    ......
    ......
    ......
    s.....

    == D 1 ==

    ..T...
    .H....
    ......
    ......
    s.....

    == R 4 ==

    ..T...
    ..H...
    ......
    ......
    s.....

    ..T...
    ...H..
    ......
    ......
    s.....

    ......
    ...TH.
    ......
    ......
    s.....

    ......
    ....TH
    ......
    ......
    s.....

    == D 1 ==

    ......
    ....T.
    .....H
    ......
    s.....

    == L 5 ==

    ......
    ....T.
    ....H.
    ......
    s.....

    ......
    ....T.
    ...H..
    ......
    s.....

    ......
    ......
    ..HT..
    ......
    s.....

    ......
    ......
    .HT...
    ......
    s.....

    ......
    ......
    HT....
    ......
    s.....

    == R 2 ==

    ......
    ......
    .H....  (H covers T)
    ......
    s.....

    ......
    ......
    .TH...
    ......
    s.....

    After simulating the rope, you can count up all of the positions the tail visited at least once.
    In this diagram, s again marks the starting position (which the tail also visited) and # marks
    other positions the tail visited:

    ..##..
    ...##.
    .####.
    ....#.
    s###..

    So, there are 13 positions the tail visited at least once.

    Simulate your complete hypothetical series of motions. How many positions does the tail of the
    rope visit at least once?
    """
    DIRECTIONS = {
        'R': (1, 0,),
        'D': (0, -1,),
        'L': (-1, 0,),
        'U': (0, 1,),
    }
    rope = Rope(head=Point(0, 0), tail=Point(0, 0))
    points_covered = set()
    for command in commands:
        print(f'== {command.direction} {command.magnitude} ==')
        dx, dy = DIRECTIONS[command.direction]
        for i in range(command.magnitude):
            points_covered.add(rope.tail)
            print_rope(rope, Point(0, 0), Point(6, 5), points_covered)
            rope.head.x += dx
            rope.head.y += dy
            rope.tail = calculate_tail_move(rope.head, rope.tail)
    points_covered.add(rope.tail)
    print(len(points_covered))


def main2(commands):
    """
    --- Part Two ---

    A rope snaps! Suddenly, the river is getting a lot closer than you remember. The bridge is still
    there, but some of the ropes that broke are now whipping toward you as you fall through the
    air!

    The ropes are moving too quickly to grab; you only have a few seconds to choose how to arch your
    body to avoid being hit. Fortunately, your simulation can be extended to support longer ropes.

    Rather than two knots, you now must simulate a rope consisting of ten knots. One knot is still
    the head of the rope and moves according to the series of motions. Each knot further down the
    rope follows the knot in front of it using the same rules as before.

    Using the same series of motions as the above example, but with the knots marked H, 1, 2, ...,
    9, the motions now occur as follows:
    """
    DIRECTIONS = {
        'R': (1, 0,),
        'D': (0, -1,),
        'L': (-1, 0,),
        'U': (0, 1,),
    }
    chain = Chain(links=[Point(0, 0) for _ in range(10)])
    points_covered = set()
    for command in commands:
        print(f'== {command.direction} {command.magnitude} ==')
        dx, dy = DIRECTIONS[command.direction]
        for i in range(command.magnitude):
            # l = [H, a, b, c, d, T]
            # [H, a], [a, b], [b, c], [c, d], [d, T]
            chain.links[0] = Point(chain.links[0].x + dx, chain.links[0].y + dy)
            for i in range(len(chain.links) - 1):
                chain.links[i + 1] = calculate_tail_move(chain.links[i], chain.links[i + 1])
            # print_chain(chain, Point(0, 0), Point(6, 5), points_covered)
            print_chain(chain, Point(0, 0), Point(25, 21), points_covered)
            points_covered.add(chain.links[-1])
    points_covered.add(chain.links[-1])
    print(len(points_covered))


def calculate_tail_move(head, tail):
    diff_x = head.x - tail.x
    diff_y = head.y - tail.y
    if abs(diff_x) <= 1 and abs(diff_y) <= 1:
        # Tail is touching or overlapping head, return existing tail
        return tail
    else:
        new_tail = Point(tail.x, tail.y)
        if abs(diff_x) >= 1:
            new_tail.x += diff_x // abs(diff_x)
        if abs(diff_y) >= 1:
            new_tail.y += diff_y // abs(diff_y)
        return new_tail


def print_rope(rope, corner1, corner2, points_covered):
    grid = []
    start = Point(0, 0,)
    for x in range(corner2.x - 1, corner1.x - 1, -1):
        for y in range(corner1.y, corner2.y):
            point = Point(x, y)
            glyph = '.'
            if point == start:
                glyph = 's'
            if point == rope.tail:
                glyph = 'T'
            if point == rope.head:
                glyph = 'H'
            if point in points_covered:
                glyph = '#'
            print(glyph, end=' ')
        print('')
    print('\n')


def print_chain(chain, corner1, corner2, points_covered):
    grid = []
    start = Point(0, 0,)
    chain_glpyhs = ['H', '1', '2', '3', '4', '5', '6', '7', '8', 'T']
    for x in range(corner2.x - 1, corner1.x - 1, -1):
        for y in range(corner1.y, corner2.y):
            point = Point(x, y)
            glyph = '.'
            if point == start:
                glyph = 's'
            for i, link in enumerate(chain.links):
                if point == link:
                    glyph = chain_glpyhs[i]
            if point in points_covered:
                glyph = '#'
            print(glyph, end=' ')
        print('')
    print('\n')


def parse(raw_input):
    def parse_line(line):
        direction, magnitude = line.split(' ')
        return Command(direction, int(magnitude))
    return [parse_line(line) for line in raw_input.split('\n')]


Command = namedtuple('Command', ['direction', 'magnitude'])


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y,))

    def __str__(self):
        return f'({self.x}, {self.y})'


@dataclass
class Rope:
    head: Point
    tail: Point


@dataclass
class Chain:
    links: list[Point]

    def __str__(self):
        return f'Chain(links={str(self.links)})'


def raw_input(filename):
    return open(filename, "r").read().rstrip("\n")


if __name__ == "__main__":
    with launch_ipdb_on_exception():
        filename = sys.argv[1]
        if len(sys.argv) > 2 and sys.argv[2] == "2":
            main2(parse(raw_input(filename)))
        else:
            main(parse(raw_input(filename)))
