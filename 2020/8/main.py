import sys
import re
import functools
from copy import deepcopy

from kitchen_sink import u


def load(filename):
    return parse(u(open(filename, 'rb').read()[:-1]))


def parse(input_text):
    program = []
    for line in input_text.split('\n'):
        instruction, arg = line.rstrip('\n').split(' ')
        program.append((instruction, int(arg)))
    return program


def run(program):
    accumulator = 0
    instructionPointer = 0
    visited = [False] * len(program)
    completed = False

    while True:
        if instructionPointer >= len(program):
            completed = True
            break
        elif visited[instructionPointer]:
            break
        visited[instructionPointer] = True
        instruction, arg = program[instructionPointer]
        if instruction == 'jmp':
            instructionPointer += arg
            continue
        elif instruction == 'acc':
            accumulator += arg
        elif instruction == 'nop':
            pass
        else:
            raise Exception(f'Unknown instruction {instruction}')
        instructionPointer += 1
        print(f'iP: {instructionPointer}, acc: {accumulator}')

    return accumulator, completed


def run_until_fixed(program):
    for i, line in enumerate(program):
        if line[0] in ('jmp', 'nop'):
            program2 = deepcopy(program)
            program2[i] = ('jmp' if line[0] == 'nop' else 'nop', line[1],)
            result = run(program2)
            if result[1]:
                return i, result


TEST_INPUT = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""
def test():
    program = parse(TEST_INPUT)
    assert run(program) == (5, False)
    print('PASS')

