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


def process_input(phase, program_input, registers):
    print(f'processing with {phase} {program_input}')
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

    index = 0
    while True:
        # print(f'{index} out of {len(registers)}-1')
        # print(registers)

        # zero pad the instruction
        instruction = f'{registers[index]:05}'
        opcode = int(instruction[3:])
        first_param_mode = int(instruction[2])
        second_param_mode = int(instruction[1])
        third_param_mode = int(instruction[0])
        # print(instruction)

        if opcode == BREAK_OP:
            print('break opcode found')
            return the_output
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
            print('Done processing')
            break


if __name__ == '__main__':
    with open("07_input.txt","r") as file:
        lines = file.read().split('\n')[0]

    # lines='3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0'
    registers = [int(x) for x in lines.split(',')]

    out_max = None
    option_max = []

    phase_options = list(permutations([0,1,2,3,4]))
    for option in phase_options:
    # for option in [(4,3,2,1,0)]:
        print(f'Processing phase setting: {option}')

        out_a = process_input(phase=option[0], program_input=0, registers=deepcopy(registers))
        out_b = process_input(phase=option[1], program_input=out_a, registers=deepcopy(registers))
        out_c = process_input(phase=option[2], program_input=out_b, registers=deepcopy(registers))
        out_d = process_input(phase=option[3], program_input=out_c, registers=deepcopy(registers))
        out_e = process_input(phase=option[4], program_input=out_d, registers=deepcopy(registers))

        if not out_max or out_e > out_max:
            out_max = out_e
            option_max = option

    print(f'max signal: {out_max}, option: {option_max}')