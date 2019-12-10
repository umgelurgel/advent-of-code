
if __name__ == '__main__':
    with open("09_input.txt","r") as file:
        lines = file.read().split('\n')[0]

    # lines = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
    registers = [int(x) for x in lines.split(',')] + [0] * 100
    user_input = 1

    ADD_OP = 1
    MULT_OP = 2
    SAVE_OP = 3
    OUTPUT_OP = 4
    JUMP_TRUE_OP = 5
    JUMP_FALSE_OP = 6
    LESS_THAN_OP = 7
    EQUALS_OP = 8
    BASE_OFFSET_OP = 9
    BREAK_OP = 99


    def get_operand(mode, index, registers, relative_base):
        POSITION_MODE = 0
        IMMEDIATE_MODE = 1
        RELATIVE_MODE = 2

        register_val = registers[index]
        if mode == POSITION_MODE:
            return registers[register_val]
        elif mode == RELATIVE_MODE:
            return registers[relative_base + register_val]
        elif mode == IMMEDIATE_MODE:
            return register_val
        else:
            import ipdb; ipdb.set_trace()
            raise Exception

    index = 0
    relative_base = 0
    while True:
        print(f'{index} out of {len(registers)-1}')
        # print(registers)

        # zero pad the instruction
        instruction = f'{registers[index]:05}'
        opcode = int(instruction[3:])
        first_param_mode = int(instruction[2])
        second_param_mode = int(instruction[1])
        third_param_mode = int(instruction[0])
        print(instruction)

        if opcode == BREAK_OP:
            import ipdb; ipdb.set_trace()
            print('break opcode found')
            break
        elif opcode == ADD_OP:
            left = get_operand(first_param_mode, index+1, registers, relative_base=relative_base)
            right = get_operand(second_param_mode, index+2, registers, relative_base=relative_base)
            target_ix = registers[index + 3]

            registers[target_ix] = left + right
            index += 4
        elif opcode == MULT_OP:
            left = get_operand(first_param_mode, index+1, registers, relative_base=relative_base)
            right = get_operand(second_param_mode, index+2, registers, relative_base=relative_base)
            target_ix = registers[index + 3]

            registers[target_ix] = left * right
            index += 4
        elif opcode == SAVE_OP:
            save_ix = registers[index + 1]
            registers[save_ix] = user_input
            index += 2
        elif opcode == OUTPUT_OP:
            left = get_operand(first_param_mode, index+1, registers, relative_base=relative_base)
            print(f'outputting: {left}')
            index += 2
        elif opcode == JUMP_TRUE_OP:
            condition = get_operand(first_param_mode, index+1, registers, relative_base=relative_base)
            instruction_pointer = get_operand(second_param_mode, index+2, registers, relative_base=relative_base)

            if condition != 0:
                index = instruction_pointer
            else:
                index += 3
        elif opcode == JUMP_FALSE_OP:
            condition = get_operand(first_param_mode, index + 1, registers, relative_base=relative_base)
            instruction_pointer = get_operand(second_param_mode, index + 2, registers, relative_base=relative_base)

            if condition == 0:
                index = instruction_pointer
            else:
                index += 3
        elif opcode == LESS_THAN_OP:
            left = get_operand(first_param_mode, index + 1, registers, relative_base=relative_base)
            right = get_operand(second_param_mode, index + 2, registers, relative_base=relative_base)
            target_ix = registers[index + 3]

            registers[target_ix] = int(left < right)
            index += 4

        elif opcode == EQUALS_OP:
            left = get_operand(first_param_mode, index + 1, registers, relative_base=relative_base)
            right = get_operand(second_param_mode, index + 2, registers, relative_base=relative_base)
            target_ix = registers[index + 3]

            registers[target_ix] = int(left == right)
            index += 4
        elif opcode == BASE_OFFSET_OP:
            left = get_operand(first_param_mode, index + 1, registers, relative_base=relative_base)
            relative_base += left
            index += 2
        else:
            print('error!')
            break


    print('program terminated')
