import sys
import re
import functools
import itertools
from collections import defaultdict, Counter
from copy import deepcopy

from kitchen_sink import u


def load(filename):
    return parse(u(open(filename, 'rb').read()[:-1]))


def parse(input_text):
    a, b, c = input_text.split('\n\n')
    return parse_rules(a), parse_your_ticket(b), parse_nearby_tickets(c)


def parse_rules(text):
    rules = {}
    for r in text.split('\n'):
        _, name, l1, h1, l2, h2, _ = re.split(
            r'^([^:]+): (\d+)-(\d+) or (\d+)-(\d+)$', r)
        rules[name] = ((int(l1), int(h1),), (int(l2), int(h2),),)
    return rules


def parse_your_ticket(text):
    _, values = text.split('your ticket:\n')
    return tuple(int(v) for v in values.split(','))


def parse_nearby_tickets(text):
    _, values = text.split('nearby tickets:\n')
    return [tuple(int(v) for v in row.split(','))
            for row in values.split('\n')]


def invalid_ticket_values(rules, tickets):
    for ticket in tickets:
        for value in ticket:
            if not any(validate(value, constraints)
                       for constraints in rules.values()):
                yield value


def valid_tickets(rules, tickets):
    for ticket in tickets:
        valid = True
        for value in ticket:
            if not any(validate(value, constraints)
                       for constraints in rules.values()):
                valid = False
                break
        if valid:
            yield ticket


def validate(value, constraints):
    (l1, h1), (l2, h2) = constraints
    return l1 <= value <= h1 or l2 <= value <= h2


def field_to_column_by_elimination(rules, tickets):
    # iterate each ticket,
    # find a ticket with a value that only fits in one of the columns,
    # map that column with its field name
    # continue until all columns mapped
    mapping = {}
    for ti, ticket in enumerate(tickets):
        for i, value in enumerate(ticket):
            print(f'Ticket #{ti}:{i:02d}')
            matches = {col: validate(value, constraints)
                       for col, constraints in rules.items()
                       if col not in mapping}
            print(f'  {dict(Counter(matches.values()))}')
            if one(matches.values()):
                col = {v: k for k, v in matches.items()}[True]
                mapping[col] = i
    return mapping


def one(iterable):
    return dict(Counter(iterable)).get(True) == 1


def field_to_column_heuristic(rules, tickets):
    """This didn't help, the columns fuzz out quite evenly :-/"""
    fuzzy = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for ticket in tickets:
        for i, value in enumerate(ticket):
            for col, constraints in rules.items():
                (l1, h1), (l2, h2) = constraints
                if l1 <= value <= h1 or l2 <= value <= h2:
                    fuzzy[col][i][0] += 1
                else:
                    fuzzy[col][i][1] += 1
    return fuzzy


TEST_INPUT = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""
def test():
    rules, your_ticket, nearby_tickets = parse(TEST_INPUT)
    all_tickets = [your_ticket] + nearby_tickets
    assert sum(invalid_ticket_values(rules, all_tickets)) == 71
    print('PASS')

