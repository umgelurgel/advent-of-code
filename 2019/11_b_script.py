
if __name__ == '__main__':
    with open("11_input.txt","r") as file:
        lines = file.read().split('\n')[0]

    registers = [int(x) for x in lines.split(',')] + [0] * 1000

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

    # Paint robot constants
    COLOR_MODE = 1
    MOVE_MODE = 2

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    BLACK = 0
    WHITE = 1

    user_input = WHITE
    pos = (0,0)
    direction = UP
    visited = set()
    current_mode = COLOR_MODE
    color_map = {
        pos: WHITE,
    }

    index = 0
    relative_base = 0
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
            if current_mode == COLOR_MODE:
                current_mode = MOVE_MODE
                visited.add(pos)
                color_map[pos] = left
                # print(f'painting {left}')

            elif current_mode == MOVE_MODE:
                current_mode = COLOR_MODE
                # Handle turn left
                if left == 0:
                    direction = (direction - 1) % 4
                # Handle turn right
                elif left == 1:
                    direction = (direction + 1) % 4
                else:
                    import ipdb; ipdb.set_trace()

                if direction == UP:
                    pos = (pos[0], pos[1] + 1)
                elif direction == RIGHT:
                    pos = (pos[0] + 1, pos[1])
                elif direction == DOWN:
                    pos = (pos[0], pos[1] -1 )
                elif direction == LEFT:
                    pos = (pos[0] -1 , pos[1])
                else:
                    import ipdb; ipdb.set_trace()

                user_input = color_map.get(pos, BLACK)
            else:
                import ipdb; ipdb.set_trace()

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
            break

    # find the size of the painting
    points = list(visited)
    width = abs(max([x[0] for x in points]) - min([x[0] for x in points]))
    height = abs(max([x[1] for x in points]) - min([x[1] for x in points]))
    output = []
    for i in range(height + 1):
        output.append([BLACK] * (width + 1))

    for point in points:
        # print(point[1])
        # output[point[1]][point[0]] = WHITE
        # print(point)
        output[abs(point[1])][point[0]] = color_map[point]
        # output[height + point[1]][point[0]] = color_map[point]

    for i in range(0, height+1):
        print(''.join([str(x) for x in output[i]]).replace(str(BLACK), ' ').replace(str(WHITE), '#'))

    print(f'visited {len(visited)} points')
