import sys
import re
from collections import Counter

from kitchen_sink import u

def traverse(data, position, slope):
    x, y = position
    width = len(data[0])
    while y < len(data):
      yield data[y][x % width]
      x += slope[0]
      y += slope[1]


def load(filename):
    return [u(line).rstrip('\n') for line in open(filename, 'rb').readlines()]


if __name__ == '__main__':
    data = load(sys.argv[1])
    slope = (int(sys.argv[2]), int(sys.argv[3]))
    print(sum(1 if char == '#' else 0
              for char in traverse(data, (0, 0), slope)))

