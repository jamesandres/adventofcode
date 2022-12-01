import sys
import re
from collections import Counter
from kitchen_sink import u

def valid_passwords(data):
    for first, second, char, password in data:
        if (password[first - 1] == char) != (password[second - 1] == char):
            yield password


def parse(line):
    parts = re.split(rb'^(\d+)-(\d+)\s+([^:]): (.*)$', line)
    return (int(parts[1]), int(parts[2]), u(parts[3]), u(parts[4]))

def load(filename):
    return [parse(line) for line in open(filename, 'rb').readlines()]


if __name__ == '__main__':
    data = load(sys.argv[1])
    print(len(list(valid_passwords(data))))

