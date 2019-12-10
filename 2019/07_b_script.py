from copy import deepcopy
from itertools import permutations

def input_generator(first, second):
    yield first
    while True:
        yield second


def get_operand(mode, index, registers):
    POSITION_MODE = 0
    IMMEDIATE_MODE = 1

    register_val = registers[index]
    if mode == POSITION_MODE:
        return registers[register_val]
    elif mode == IMMEDIATE_MODE:
        return register_val
    else:
        import ipdb; ipdb.set_trace()
        raise Exception


def process_input(phase, program_input, registers, index):
    print(f'processing with phase: {phase}, input: {program_input}, index: {index}')
    ADD_OP = 1
    MULT_OP = 2
    SAVE_OP = 3
    OUTPUT_OP = 4
    JUMP_TRUE_OP = 5
    JUMP_FALSE_OP = 6
    LESS_THAN_OP = 7
    EQUALS_OP = 8
    BREAK_OP = 99

    user_input = input_generator(phase, program_input)
    the_output = None

    while True:
        # print(f'{index} out of {len(registers)-1}')
        # print(registers)

        # zero pad the instruction
        instruction = f'{registers[index]:05}'
        opcode = int(instruction[3:])
        first_param_mode = int(instruction[2])
        second_param_mode = int(instruction[1])
        third_param_mode = int(instruction[0])
        # print(instruction)

        if opcode == BREAK_OP:
            print(f'break opcode found, returning {the_output}, {index+1}')

            return the_output, -1
            break
        elif opcode == ADD_OP:
            left = get_operand(first_param_mode, index+1, registers)
            right = get_operand(second_param_mode, index+2, registers)
            target_ix = registers[index + 3]

            registers[target_ix] = left + right
            index += 4
        elif opcode == MULT_OP:
            left = get_operand(first_param_mode, index+1, registers)
            right = get_operand(second_param_mode, index+2, registers)
            target_ix = registers[index + 3]

            registers[target_ix] = left * right
            index += 4
        elif opcode == SAVE_OP:
            save_ix = registers[index + 1]
            registers[save_ix] = next(user_input)
            index += 2
        elif opcode == OUTPUT_OP:
            output_ix = registers[index + 1]
            # print(f'outputting: {registers[output_ix]}')
            # TEST
            # return registers[index + 1]
            the_output = registers[output_ix]
            index += 2
            return the_output, index

        elif opcode == JUMP_TRUE_OP:
            condition = get_operand(first_param_mode, index+1, registers)
            instruction_pointer = get_operand(second_param_mode, index+2, registers)

            if condition != 0:
                index = instruction_pointer
            else:
                index += 3
        elif opcode == JUMP_FALSE_OP:
            condition = get_operand(first_param_mode, index + 1, registers)
            instruction_pointer = get_operand(second_param_mode, index + 2, registers)

            if condition == 0:
                index = instruction_pointer
            else:
                index += 3
        elif opcode == LESS_THAN_OP:
            left = get_operand(first_param_mode, index + 1, registers)
            right = get_operand(second_param_mode, index + 2, registers)
            target_ix = registers[index + 3]

            registers[target_ix] = int(left < right)
            index += 4

        elif opcode == EQUALS_OP:
            left = get_operand(first_param_mode, index + 1, registers)
            right = get_operand(second_param_mode, index + 2, registers)
            target_ix = registers[index + 3]

            registers[target_ix] = int(left == right)
            index += 4
        else:
            import ipdb; ipdb.set_trace()
            print('Done processing')
            break


if __name__ == '__main__':
    with open("07_input.txt","r") as file:
        lines = file.read().split('\n')[0]

    # lines='3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'
    registers = [int(x) for x in lines.split(',')]

    out_max = None
    option_max = []

    phase_options = list(permutations([5,6,7,8,9]))
    for option in phase_options:
    # for option in [(9,8,7,6,5)]:
        print(f'Processing phase setting: {option}')

        ix_a, ix_b, ix_c, ix_d, ix_e = 0, 0, 0, 0, 0
        reg_a, reg_b, reg_c, reg_d, reg_e = deepcopy(registers), deepcopy(registers), deepcopy(registers), deepcopy(registers), deepcopy(registers)
        out_e = 0
        first_run = True
        while True:
            out_a, ix_a = process_input(
                phase=option[0] if first_run else out_e, program_input=out_e, registers=reg_a, index=ix_a
            )
            if ix_a == -1:
                break
            out_b, ix_b = process_input(
                phase=option[1] if first_run else out_a, program_input=out_a, registers=reg_b, index=ix_b
            )
            out_c, ix_c = process_input(
                phase=option[2] if first_run else out_b, program_input=out_b, registers=reg_c, index=ix_c
            )
            out_d, ix_d = process_input(
                phase=option[3] if first_run else out_c, program_input=out_c, registers=reg_d, index=ix_d
            )
            out_e, ix_e = process_input(
                phase=option[4] if first_run else out_d, program_input=out_d, registers=reg_e, index=ix_e
            )

            first_run = False

        if not out_max or out_e > out_max:
            out_max = out_e
            option_max = option

    print(f'max signal: {out_max} option: {option_max}')