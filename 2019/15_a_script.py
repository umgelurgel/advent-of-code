import random

if __name__ == '__main__':
    with open("15_input.txt","r") as file:
        lines = file.read().split('\n')[0]

    registers = [int(x) for x in lines.split(',')] + [0] * 100

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

    def print_map(tiles, current_pos):
        # print(tiles)
        # print(current_pos)
        points = tiles.keys()
        width = abs(max([x[0] for x in points]) - min([x[0] for x in points]))
        height = abs(max([x[1] for x in points]) - min([x[1] for x in points]))
        x_offset = min([x[0] for x in points])
        y_offset = min([x[1] for x in points])
        output = []
        for i in range(height + 1):
            output.append([' '] * (width + 1))

        for point in points:
            x = point[0] + abs(x_offset)
            y = point[1] + abs(y_offset)
            if point == current_pos:
                output[y][x] = 'D'
            else:
                # print(point[1])
                # output[point[1]][point[0]] = WHITE
                # print(point)
                output[y][x] = tiles[point]
                # output[height + point[1]][point[0]] = color_map[point]

        for i in range(0, height + 1):
            print(''.join([str(x) for x in output[i]]))

        print('')
        # input()

    current_pos = (0,0)
    tiles = {
        current_pos: '.'
    }

    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4
    direction_names = {
        1: 'NORTH',
        2: 'SOUTH',
        3: 'WEST',
        4: 'EAST',
    }

    WALL = 0
    MOVED = 1
    REPAIR = 2

    user_input = NORTH
    print('Moving NORTH')

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
            registers[save_ix] = user_input
            index += 2
        elif opcode == OUTPUT_OP:
            left = get_operand(first_param_mode, index+1, registers, relative_base=relative_base)

            # NORTH = 1
            # SOUTH = 2
            # WEST = 3
            # EAST = 4

            if left == WALL:
                if user_input == NORTH:
                    next_pos = (current_pos[0], current_pos[1] + 1)
                    # user_input = EAST
                    user_input = random.choice([2,3,4])
                    print(f'Hit wall moving NORTH from {current_pos} to {next_pos}, changing direction to {direction_names[user_input]}.')
                elif user_input == EAST:
                    next_pos = (current_pos[0] + 1, current_pos[1])
                    # user_input = SOUTH
                    user_input = random.choice([1,2,3])
                    print(f'Hit wall moving EAST from {current_pos} to {next_pos}, changing direction to {direction_names[user_input]}.')
                elif user_input == SOUTH:
                    next_pos = (current_pos[0], current_pos[1] - 1)
                    # user_input = WEST
                    user_input = random.choice([1,3,4])
                    print(f'Hit wall moving SOUTH from {current_pos} to {next_pos}, changing direction to {direction_names[user_input]}.')
                elif user_input == WEST:
                    next_pos = (current_pos[0] - 1, current_pos[1])
                    # user_input = NORTH
                    user_input = random.choice([1,2,4])
                    print(f'Hit wall moving WEST from {current_pos} to {next_pos}, changing direction to {direction_names[user_input]}.')

                tiles[next_pos] = '#'
            elif left == MOVED:
                if user_input == NORTH:
                    user_input = random.choice([1,3,4])
                    next_pos = (current_pos[0], current_pos[1] + 1)
                elif user_input == EAST:
                    user_input = random.choice([1,2,4])
                    next_pos = (current_pos[0] + 1, current_pos[1])
                elif user_input == SOUTH:
                    user_input = random.choice([2,3,4])
                    next_pos = (current_pos[0], current_pos[1] - 1)
                elif user_input == WEST:
                    user_input = random.choice([1,2,3])
                    next_pos = (current_pos[0] - 1, current_pos[1])

                tiles[current_pos] = '.'
                tiles[next_pos] = '.'
                current_pos = next_pos
            elif left == REPAIR:
                if user_input == NORTH:
                    user_input = random.choice([1,3,4])
                    next_pos = (current_pos[0], current_pos[1] + 1)
                elif user_input == EAST:
                    user_input = random.choice([1,2,4])
                    next_pos = (current_pos[0] + 1, current_pos[1])
                elif user_input == SOUTH:
                    user_input = random.choice([2,3,4])
                    next_pos = (current_pos[0], current_pos[1] - 1)
                elif user_input == WEST:
                    user_input = random.choice([1,2,3])
                    next_pos = (current_pos[0] - 1, current_pos[1])

                tiles[current_pos] = '.'
                tiles[next_pos] = 'O'
                # current_pos = next_pos
                import ipdb; ipdb.set_trace()
            else:
                import ipdb; ipdb.set_trace()

            print_map(tiles, current_pos)

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

    blocks = [x for x in tiles.values() if x == 2]
    print(f'There are {len(blocks)} blocks')

