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

    registers = [0] * 4

    ops = [
        # ADDR
        lambda regs, op, arg1, arg2, out_reg_id: [*regs[0:out_reg_id], regs[arg1] + regs[arg2], *regs[out_reg_id + 1:]],
        # ADDI
        lambda regs, op, arg1, arg2, out_reg_id: [*regs[0:out_reg_id], regs[arg1] + arg2, *regs[out_reg_id + 1:]],

        # MULR
        lambda regs, op, arg1, arg2, out_reg_id: [*regs[0:out_reg_id], regs[arg1] * regs[arg2], *regs[out_reg_id + 1:]],
        # MULI
        lambda regs, op, arg1, arg2, out_reg_id: [*regs[0:out_reg_id], regs[arg1] * arg2, *regs[out_reg_id + 1:]],

        # BANR
        lambda regs, op, arg1, arg2, out_reg_id: [*regs[0:out_reg_id], regs[arg1] & regs[arg2], *regs[out_reg_id + 1:]],
        # BANI
        lambda regs, op, arg1, arg2, out_reg_id: [*regs[0:out_reg_id], regs[arg1] & arg2, *regs[out_reg_id + 1:]],

        # BORR
        lambda regs, op, arg1, arg2, out_reg_id: [*regs[0:out_reg_id], regs[arg1] | regs[arg2], *regs[out_reg_id + 1:]],
        # BORI
        lambda regs, op, arg1, arg2, out_reg_id: [*regs[0:out_reg_id], regs[arg1] | arg2, *regs[out_reg_id + 1:]],

        # SETR
        lambda regs, op, arg1, arg2, out_reg_id: [*regs[0:out_reg_id], regs[arg1], *regs[out_reg_id + 1:]],
        # SETI
        lambda regs, op, arg1, arg2, out_reg_id: [*regs[0:out_reg_id], arg1, *regs[out_reg_id + 1:]],

        # GTIR
        lambda regs, op, arg1, arg2, out_reg_id: [*regs[0:out_reg_id], 1 if arg1 > regs[arg2] else 0, *regs[out_reg_id + 1:]],
        # GTRI
        lambda regs, op, arg1, arg2, out_reg_id: [*regs[0:out_reg_id], 1 if regs[arg1] > arg2 else 0, *regs[out_reg_id + 1:]],
        # GTRR
        lambda regs, op, arg1, arg2, out_reg_id: [*regs[0:out_reg_id], 1 if regs[arg1] > regs[arg2] else 0, *regs[out_reg_id + 1:]],

        # EQIR
        lambda regs, op, arg1, arg2, out_reg_id: [*regs[0:out_reg_id], 1 if arg1 == regs[arg2] else 0, *regs[out_reg_id + 1:]],
        # EQRI
        lambda regs, op, arg1, arg2, out_reg_id: [*regs[0:out_reg_id], 1 if regs[arg1] == arg2 else 0, *regs[out_reg_id + 1:]],
        # EQRR
        lambda regs, op, arg1, arg2, out_reg_id: [*regs[0:out_reg_id], 1 if regs[arg1] == regs[arg2] else 0, *regs[out_reg_id + 1:]],
    ]

    three_counter = 0
    for before, instruction, after in sample_instructions:
        match_counter = 0
        for op in ops:
            if op(before, *instruction) == after:
                match_counter += 1

        if match_counter >= 3:
            three_counter += 1

    print(three_counter)