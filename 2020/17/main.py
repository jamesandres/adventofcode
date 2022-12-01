import sys
import re
import functools
import itertools
from collections import defaultdict, Counter
from copy import deepcopy

from kitchen_sink import u


class Space:
    """A 3D space for Conway type stuffs."""
    def __init__(self, space=None):
        self.space = space or {}
        self.dim = {'x': [0, 0], 'y': [0, 0], 'z': [0, 0]}

    @classmethod
    def parse(cls, text_slice):
        space = cls()
        for y, line in enumerate(text_slice.split('\n')):
            for x, value in enumerate(line):
                if value == '#':
                    space.set(x, y, 0, '#')
        return space
    
    def get(self, x, y, z):
        try:
            return self.space[z][y][x]
        except KeyError:
            return '.'

    def set(self, x, y, z, value):
        if z not in self.space:
            self.space[z] = {}
        if y not in self.space[z]:
            self.space[z][y] = {}
        # TODO: This is a bit lazy, we're only ever pushing the max
        #       farther out and pulling the min farther down. Probably
        #       that's how the modelling goes anyway so not a great
        #       harm to performance.
        for axis, axis_value in (('z', z), ('y', y), ('x', x)):
            self.dim[axis] = [min(self.dim[axis][0], axis_value),
                              max(self.dim[axis][1], axis_value)]
        self.space[z][y][x] = value

    def points(self):
        """All points in the interesting box of space"""
        (_, (xl, xh)), (_, (yl, yh)), (_, (zl, zh)) = self.dim.items()
        for z in range(zl - 1 , zh + 2):
            for y in range(yl - 1, yh + 2):
                for x in range(xl - 1, xh + 2):
                    yield x, y, z, self.get(x, y, z)
    
    def num_active_neighbours(self, x, y, z):
        counter = 0
        for dz in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if (dx, dy, dz) == (0, 0, 0):
                        continue
                    nx = x + dx
                    ny = y + dy
                    nz = z + dz
                    value = self.get(x + dx, y + dy, z + dz)
                    print(f'({nx}, {ny}, {nz}) is {repr(value)}')
                    if value == '#':
                        counter += 1
        return counter

    def count_active(self):
        return len([p for p in self.points() if p[3] == '#'])

    def plot(self):
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        x, y, z, _ = unzip([p for p in self.points() if p[3] == '#'])

        ax.scatter(x, y, z, c='r', marker='o')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        plt.show()


def unzip(zipped):
    return list(zip(*zipped))


def boot(space):
    for _ in range(6):
        space = cycle(space)
    return space.count_active()


def cycle(space):
    next_space = Space()
    for x, y, z, value in space.points():
        num_active = space.num_active_neighbours(x, y, z)
        print(f'{x=},{y=},{z=},{value=},{num_active=}')
        # (1) If a cube is active and exactly 2 or 3 of its neighbors
        #     are also active, the cube remains active. Otherwise,
        #     the cube becomes inactive.
        if value == '#' and (2 > num_active > 3):
            next_space.set(x, y, z, '.')
        # (2) If a cube is inactive but exactly 3 of its neighbors
        #     are active, the cube becomes active. Otherwise, the
        #     cube remains inactive.
        elif value == '.' and num_active == 3:
            next_space.set(x, y, z, '#')
    return next_space


def load(filename):
    return Space.parse(u(open(filename, 'rb').read()[:-1]))



TEST_INPUT = """.#.
..#
###"""
def test():
    space = Space.parse(TEST_INPUT)
    assert boot(space) == 112
    print('PASS')

