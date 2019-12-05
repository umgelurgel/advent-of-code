
if __name__ == '__main__':
    with open("05_a_input.txt","r") as file:
        lines = file.read().split('\n')[0]

    registers = [int(x) for x in lines.split(',')]

    # for part 1
    # user_input = 1
    # fort part 2
    user_input = 5

    ADD_OP = 1
    MULT_OP = 2
    SAVE_OP = 3
    OUTPUT_OP = 4
    JUMP_TRUE_OP = 5
    JUMP_FALSE_OP = 6
    LESS_THAN_OP = 7
    EQUALS_OP = 8
    BREAK_OP = 99

    POSITION_MODE = 0
    IMMEDIATE_MODE = 1

    def get_operand(mode, index, registers):
        register_val = registers[index]
        if mode == POSITION_MODE:
            return registers[register_val]
        elif mode == IMMEDIATE_MODE:
            return register_val
        else:
            import ipdb; ipdb.set_trace()
            raise Exception

    index = 0
    while True:
        # print(f'{index} out of {len(registers)}')
        # print(registers)

        # zero pad the instruction
        instruction = f'{registers[index]:05}'
        opcode = int(instruction[3:])
        first_param_mode = int(instruction[2])
        second_param_mode = int(instruction[1])
        third_param_mode = int(instruction[0])
        print(instruction)

        if opcode == BREAK_OP:
            print('break opcode found')
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
            registers[save_ix] = user_input
            index += 2
        elif opcode == OUTPUT_OP:
            output_ix = registers[index + 1]
            print(f'outputting: {registers[output_ix]}')
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
            print('error!')
            break


    print('program terminated')
