import sys
import re
import functools
from itertools import combinations
from copy import deepcopy
from collections import defaultdict

from kitchen_sink import u


def load(filename):
    return parse(u(open(filename, 'rb').read()[:-1]))


def parse(input_text):
    return [parse_instruction(instr) for instr in input_text.split('\n')]


def parse_instruction(instr):
    var, value = instr.split(' = ')
    if var == 'mask':
        zeros_mask = 0
        ones_mask = 0
        for i, b in enumerate(reversed(value)):
            if b == '0':
                zeros_mask += 1 << i
            elif b == '1':
                ones_mask += 1 << i
        return ('mask', None, (zeros_mask, ones_mask))
    elif var.startswith('mem['):
        address = int(var[4:-1])  # drop the 'mem[' and ']'
        return ('mem', address, int(value))
    else:
        raise Exception(f'Unknown instruction type {instr}')


def run(instructions):
    memory = defaultdict(int)
    mask = None

    for instr_type, address, value in instructions:
        if instr_type == 'mask':
            mask = value
        elif instr_type == 'mem':
            memset(memory, address, value, mask)
        else:
            raise Exception(f'Unknown instruction type {instr_type}')
    return sum(memory.values())


def memset(memory, address, value, mask):
    memory[address] = bitmask(mask, value)


def bitmask(mask, value):
    zeros_mask, ones_mask = mask
    return value & ~(zeros_mask) | ones_mask



TEST_INPUT = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""
def test():
    instructions = parse(TEST_INPUT)
    assert run(instructions) == 165
    print('PASS')

