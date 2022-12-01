import sys
import re
import functools

from kitchen_sink import u


def load(filename):
    return [parse(u(record)) for record in open(filename, 'rb').read()[:-1].split(b'\n\n')]


def parse(record):
    return [set(person) for person in record.split('\n')]


def intersect(data):
    for record in data:
        intersection = functools.reduce(lambda acc, person:
                                        acc.intersection(person),
                                        record)
        yield intersection


if __name__ == '__main__':
    data = load(sys.argv[1])
    print(sum([len(s) for s in intersect(data)]))
