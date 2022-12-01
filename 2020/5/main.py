import sys
import re

from kitchen_sink import u


def print_seats(data):
    """
    Lazy way to find hole in the data, just visualise it :-/
    """
    max_row = max(record[0] for record in data)
    max_col = max(record[1] for record in data)
    output = [[' ' for x in range(max_col)] for y in range(max_row)]
    for record in data:
        row, col, _ = record
        output[row - 1][col - 1] = '#'
    print('\n'.join([str(i + 1) + ' ' + ''.join(line) for i, line in enumerate(output)]))


def load(filename):
    return [parse(u(line.rstrip(b'\n'))) for line in open(filename, 'rb').readlines()]


def parse(line):
    row, col = line[:7], line[-3:]
    row = int(row.translate({ord('F'): ord('0'), ord('B'): ord('1')}), 2)
    col = int(col.translate({ord('L'): ord('0'), ord('R'): ord('1')}), 2)
    seat_id = row * 8 + col
    return (row, col, seat_id)

def test():
    assert parse('FBFBBFFRLR') == (44, 5, 357)
    assert parse('BFFFBBFRRR') == (70, 7, 567)
    assert parse('FFFBBBFRRR') == (14, 7, 119)
    assert parse('BBFFBBFRLL') == (102, 4, 820)
    print('PASS')

if __name__ == '__main__':
    data = load(sys.argv[1])
    print(max(record[2] for record in data))
