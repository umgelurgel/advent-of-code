from collections import deque
from datetime import datetime


if __name__ == '__main__':
    with open("input.txt", "r") as file:
        # Remove empty lines
        lines = [line for line in file.read().split('\n') if line]

    sample_instructions = []
    # Lines 0-2331 are sample instructions; lines 2331:end are actual instructions
    for i in range(0, 2331, 3):
        if lines[i].startswith('Before: '):
            before = eval(lines[i].replace('Before: ', ''))
            instruction = [int(x) for x in lines[i + 1].split(' ')]
            after = eval(lines[i + 2].replace('After:  ', ''))
            sample_instructions.append((before, instruction, after))

    actual_instructions = []
    for line in lines[2331:]:
        actual_instructions.append([int(x) for x in line.split(' ')])

    def addr(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], regs[arg1] + regs[arg2], *regs[out_reg_id + 1:]]
    def addi(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], regs[arg1] + arg2, *regs[out_reg_id + 1:]]

    def mulr(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], regs[arg1] * regs[arg2], *regs[out_reg_id + 1:]]
    def muli(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], regs[arg1] * arg2, *regs[out_reg_id + 1:]]

    def banr(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], regs[arg1] & regs[arg2], *regs[out_reg_id + 1:]]
    def bani(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], regs[arg1] & arg2, *regs[out_reg_id + 1:]]

    def borr(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], regs[arg1] | regs[arg2], *regs[out_reg_id + 1:]]
    def bori(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], regs[arg1] | arg2, *regs[out_reg_id + 1:]]

    def setr(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], regs[arg1], *regs[out_reg_id + 1:]]
    def seti(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], arg1, *regs[out_reg_id + 1:]]

    def gtir(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], 1 if arg1 > regs[arg2] else 0, *regs[out_reg_id + 1:]]
    def gtri(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], 1 if regs[arg1] > arg2 else 0, *regs[out_reg_id + 1:]]
    def gtrr(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], 1 if regs[arg1] > regs[arg2] else 0, *regs[out_reg_id + 1:]]

    def eqir(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], 1 if arg1 == regs[arg2] else 0, *regs[out_reg_id + 1:]]
    def eqri(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], 1 if regs[arg1] == arg2 else 0, *regs[out_reg_id + 1:]]
    def eqrr(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], 1 if regs[arg1] == regs[arg2] else 0, *regs[out_reg_id + 1:]]

    ops = [
        addr,
        addi,

        mulr,
        muli,

        banr,
        bani,

        borr,
        bori,

        setr,
        seti,

        gtir,
        gtri,
        gtrr,

        eqir,
        eqri,
        eqrr,
    ]

    ops_by_id = {}

    for before, instruction, after in sample_instructions:
        matches = []
        for op_ix, op in enumerate(ops):
            if op(before, *instruction[1:]) == after:
                matches.append([instruction[0], op, op_ix])

        if len(matches) == 1:
            opcode, op, op_ix = matches[0]
            ops_by_id[opcode] = op
            del ops[op_ix]

    # sanity check
    for before, instruction, after in sample_instructions:
        op = ops_by_id[instruction[0]]
        if op(before, *instruction[1:]) != after:
            print('ERROR')

    registers = [0] * 4
    for op_id, arg1, arg2, out_reg_id in actual_instructions:
        registers = ops_by_id[op_id](registers, arg1, arg2, out_reg_id)
        print(registers)

    print(registers)
