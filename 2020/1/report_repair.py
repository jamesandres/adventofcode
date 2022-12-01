import sys
import functools
import itertools


def main(numbers, r):
    for combo in itertools.combinations(numbers, r):
        if sum(combo) == 2020:
            yield functools.reduce(lambda acc, n: acc * n, combo)


if __name__ == '__main__':
    filename = sys.argv[1]
    r = int(sys.argv[2])

    print(f'filename: {filename}, r: {r}')

    numbers = [int(line) for line in open(filename, 'rb').readlines()]
    for result in main(numbers, r):
        print(result)

