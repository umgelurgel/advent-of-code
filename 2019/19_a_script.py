from copy import deepcopy
from collections import Counter
import time

if __name__ == '__main__':
    with open("19_input.txt","r") as file:
        lines = file.read().split('\n')[0]

    orig_registers = [int(x) for x in lines.split(',')] + [0] * 10000

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

    X_MODE = 0
    Y_MODE = 1
    current_mode = X_MODE

    min_per_level = {
    }
    max_per_level = {}

    width = 500
    tile_counter = 4 * width + 2
    tiles = []
    for i in range(width):
        tiles.append([' '] * width)

    def print_tiles(tiles):
        return
        print('\n'.join([''.join(line) for line in tiles]))

    while tile_counter < width * width:
        print(f'{time.clock()}: {tile_counter} ({tile_counter/(width * width)}%)')
        registers = deepcopy(orig_registers)
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

                if current_mode == X_MODE:
                    user_input = tile_counter % width
                    current_mode = Y_MODE
                elif current_mode == Y_MODE:
                    current_mode = X_MODE
                    user_input = tile_counter // width
                else:
                    pass

                registers[save_ix] = user_input
                index += 2
            elif opcode == OUTPUT_OP:
                left = get_operand(first_param_mode, index+1, registers, relative_base=relative_base)

                x = tile_counter % width
                y = tile_counter // width
                tiles[y][x] = '#' if left else '.'
                if left:
                    max_per_level[y] = x
                    if y not in min_per_level:
                        min_per_level[y] = x

                    tile_counter += 1
                else:
                    if y in max_per_level:
                        tile_counter += width - x + min_per_level[y]

                    else:
                        tile_counter += 1
                print_tiles(tiles)

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

    import ipdb; ipdb.set_trace()
    ww = Counter(''.join([''.join(line) for line in tiles]))
    print(ww)