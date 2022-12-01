import sys
import re
import functools
import itertools
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
        return ('mask', None, value)
    elif var.startswith('mem['):
        address = int(var[4:-1])  # drop the 'mem[' and ']'
        return ('mem', address, int(value))
    else:
        raise Exception(f'Unknown instruction type {instr}')


def floating_masks(raw_mask):
    floaters = [i for i, b in enumerate(raw_mask) if b == 'X']
    for perm in itertools.product(('0', '1'), repeat=len(floaters)):
        # Bitmasking has had an unannounced changed in part 2, grrr
        # Now a mask of 0000 is meant to act as a passthru. Zeros
        # from the raw mask should be ignored. HOWEVER zeros from the
        # floating 'X's should be applied.
        mask = list(raw_mask.replace('0', '.').replace('X', '0'))
        for i, b in enumerate(perm):
            mask[floaters[i]] = b
        mask = ''.join(mask)
        yield mask_maker(mask)


def mask_maker(mask):
    zeros_mask = 0
    ones_mask = 0
    for i, b in enumerate(reversed(mask)):
        if b == '0':
            zeros_mask += 1 << i
        elif b == '1':
            ones_mask += 1 << i
    return zeros_mask, ones_mask


def run(instructions):
    memory = defaultdict(int)
    raw_mask = None

    for instr_type, address, value in instructions:
        if instr_type == 'mask':
            raw_mask = value
        elif instr_type == 'mem':
            memset(memory, address, value, raw_mask)
        else:
            raise Exception(f'Unknown instruction type {instr_type}')
    return sum(memory.values())


def memset(memory, address, value, raw_mask):
    for mask in floating_masks(raw_mask):
        mangled_address = bitmask(mask, address)
        #print('memset', address, 'mangled to', mangled_address, '<-', value)
        memory[mangled_address] = value


def bitmask(mask, value):
    zeros_mask, ones_mask = mask
    #print(f'bitmask, address    : {value:036b}')
    #print(f'bitmask, zeros_mask : {zeros_mask:036b}')
    #print(f'bitmask, ones_mask  : {ones_mask:036b}')
    result = value & ~(zeros_mask) | ones_mask
    #print(f'bitmask, result     : {result:036b}')
    return result


TEST_INPUT = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""
def test():
    instructions = parse(TEST_INPUT)
    assert run(instructions) == 208
    print('PASS')

