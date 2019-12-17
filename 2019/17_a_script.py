import random

if __name__ == '__main__':
    with open("17_input.txt","r") as file:
        lines = file.read().split('\n')[0]

    registers = [int(x) for x in lines.split(',')] + [0] * 10000

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

    POSITION_MODE = 0
    IMMEDIATE_MODE = 1
    RELATIVE_MODE = 2

    def get_operand_address(mode, index, registers, relative_base):
        register_val = registers[index]
        if mode == POSITION_MODE:
            return register_val
        elif mode == RELATIVE_MODE:
            return relative_base + register_val
        else:
            import ipdb; ipdb.set_trace()
            raise Exception

    def get_operand(mode, index, registers, relative_base):
        if mode == IMMEDIATE_MODE:
            return registers[index]

        address = get_operand_address(
            mode=mode,
            index=index,
            registers=registers,
            relative_base=relative_base,
        )
        return registers[address]

    output = []

    index = 0
    relative_base = 0
    while True:
        # print(f'{index} out of {len(registers)-1}')
        # print(registers)
        #
        # zero pad the instruction
        instruction = f'{registers[index]:05}'
        opcode = int(instruction[3:])
        first_param_mode = int(instruction[2])
        second_param_mode = int(instruction[1])
        third_param_mode = int(instruction[0])
        # print(instruction)

        if opcode == BREAK_OP:
            print('break opcode found')
            break
        elif opcode == ADD_OP:
            left = get_operand(first_param_mode, index+1, registers, relative_base=relative_base)
            right = get_operand(second_param_mode, index+2, registers, relative_base=relative_base)
            target_ix = get_operand_address(third_param_mode, index + 3, registers, relative_base=relative_base)

            registers[target_ix] = left + right
            index += 4
        elif opcode == MULT_OP:
            left = get_operand(first_param_mode, index+1, registers, relative_base=relative_base)
            right = get_operand(second_param_mode, index+2, registers, relative_base=relative_base)
            target_ix = get_operand_address(third_param_mode, index + 3, registers, relative_base=relative_base)

            registers[target_ix] = left * right
            index += 4
        elif opcode == SAVE_OP:
            save_ix = get_operand_address(first_param_mode, index + 1, registers, relative_base=relative_base)
            import ipdb; ipdb.set_trace()
            registers[save_ix] = user_input
            index += 2
        elif opcode == OUTPUT_OP:
            left = get_operand(first_param_mode, index+1, registers, relative_base=relative_base)
            output.append(left)

            # print(f'outputting: {left}')
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
            target_ix = get_operand_address(third_param_mode, index + 3, registers, relative_base=relative_base)

            registers[target_ix] = int(left < right)
            index += 4

        elif opcode == EQUALS_OP:
            left = get_operand(first_param_mode, index + 1, registers, relative_base=relative_base)
            right = get_operand(second_param_mode, index + 2, registers, relative_base=relative_base)
            target_ix = get_operand_address(third_param_mode, index + 3, registers, relative_base=relative_base)

            registers[target_ix] = int(left == right)
            index += 4
        elif opcode == BASE_OFFSET_OP:
            left = get_operand(first_param_mode, index + 1, registers, relative_base=relative_base)
            relative_base += left
            index += 2
        else:
            print('error!')

    tiles = [line for line in ''.join([str(chr(x)) for x in output]).split('\n') if line]
    for i in range(len(tiles)):
        tiles[i] = list(tiles[i])

    print('\n'.join([''.join(x) for x in tiles]))
    print('\n\n\n')

    def horizontal_scaffold(tiles, y, x):
        left = False
        if x - 1 >= 0:
            left = tiles[y][x - 1] == '#'

        right = False
        if x + 1 < len(tiles[y]):
            right = tiles[y][x + 1] == '#'

        return left and right

    def vertical_scaffold(tiles, y, x):
        up = False
        if y - 1 >= 0:
            up = tiles[y -1][x] == '#'

        down = False
        if y + 1 < len(tiles):
            down = tiles[y + 1][x] == '#'

        return up and down

    alignment = 0

    for y in range(len(tiles)):
        for x in range(len(tiles[y])):
            if tiles[y][x] == '#' and horizontal_scaffold(tiles, y, x) and vertical_scaffold(tiles, y, x):
                tiles[y][x] = 'O'
                alignment += x * y

    print('\n'.join([''.join(x) for x in tiles]))
    print(alignment)

