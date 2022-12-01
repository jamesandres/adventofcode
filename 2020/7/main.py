import sys
import re
import functools

from kitchen_sink import u


def load(filename):
    return tree(parse(u(open(filename, 'rb').read()[:-1])))


def parse(rules_text):
    rules = []
    for line in rules_text.split('\n'):
        colour, constraints_text = line.split(' bags contain ')
        for constraint_text in constraints_text.split(', '):
            if 'no other bags' in constraint_text:
                continue
            num, colour2 = re.findall(r'^(\d+)\s+(.*)\s+bag', constraint_text)[0]
            rules.append((colour, int(num), colour2,))
    return rules


class Bag:
    def __init__(self, colour):
        self.colour = colour
        self.neighbours = {}

    def __repr__(self):
        return f'Bag({repr(self.colour)})'

    def addNeighbour(self, bag, num):
        self.neighbours[bag.colour] = (bag, num,)

    def bags_count(self):
        count = 1
        for bag, num in self.neighbours.values():
            count += num * bag.bags_count()
        return count



def tree(rules):
    nodes = {}
    for a, num, b in rules:
        if a not in nodes:
            nodes[a] = Bag(a)
        if b not in nodes:
            nodes[b] = Bag(b)
        nodes[a].addNeighbour(nodes[b], num)
    return nodes



def search(rules, start, num, target, path=tuple()):
    path = path + (start,)
    if start == target:
        return path
    if not any(edge[0] == start for edge in rules):
        return None
    for edge in rules:
        if edge[0] != start:
            continue
        if edge[2] not in path:
            new_path = search(rules, edge[2], num, target, path)
            if new_path:
                return new_path
    return None


TEST_RULES = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""
def test():
    rules = parse(TEST_RULES)
    solutions = {search(rules, edge[0], 1, 'shiny gold') for edge in rules}
    solutions.remove(('shiny gold',))
    solutions.remove(None)
    assert len(solutions) == 4
    print('PASS')


TEST_RULES2 = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""


if __name__ == '__main__':
    data = load(sys.argv[1])
