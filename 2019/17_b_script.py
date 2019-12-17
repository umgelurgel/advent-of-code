import random
from collections import deque
from copy import deepcopy

if __name__ == '__main__':
    with open("17_b_input.txt","r") as file:
        lines = [line for line in file.read().split('\n') if line]

    tiles = [list(line) for line in lines]

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    direction = UP
    # find robot:
    for y in range(len(tiles)):
        for x in range(len(tiles[y])):
            if tiles[y][x] == '^':
                pos = (x, y)
                break

    print('\n'.join([''.join(x) for x in tiles]))

    def draw_tiles(tiles, pos):
        return
        tiles = deepcopy(tiles)
        tiles[pos[1]][pos[0]] = 'D'
        print('\n'.join([''.join(x) for x in tiles]))

    def tile_up(tiles, pos):
        if pos[1] - 1 >= 0:
            return tiles[pos[1] - 1][pos[0]]

    def tile_down(tiles, pos):
        if pos[1] + 1 < len(tiles):
            return tiles[pos[1] + 1][pos[0]]

    def tile_left(tiles, pos):
        if pos[0] - 1 >= 0:
            return tiles[pos[1]][pos[0] - 1]

    def tile_right(tiles, pos):
        if pos[0] + 1 < len(tiles[pos[1]]):
            return tiles[pos[1]][pos[0] + 1]

    instructions = []
    while True:
        # move as far as you can in the current direction
        # if cannot move, turn left or right

        if direction == UP:
            counter = 0
            while tile_up(tiles, pos) == '#':
                counter += 1
                pos = (pos[0], pos[1] - 1)
                draw_tiles(tiles, pos)

            if counter:
                instructions.append(counter)

            # check if it can move left, if so, turn
            if tile_left(tiles, pos) == '#':
                instructions.append('L')
                direction = LEFT
            # otherwise check if it can move right
            elif tile_right(tiles, pos) == '#':
                instructions.append('R')
                direction = RIGHT
            # otherwise reached end of input
            else:
                break

        elif direction == DOWN:
            counter = 0
            while tile_down(tiles, pos) == '#':
                counter += 1
                pos = (pos[0], pos[1] + 1)
                draw_tiles(tiles, pos)

            if counter:
                instructions.append(counter)

            # check if it can move left, if so, turn
            if tile_left(tiles, pos) == '#':
                instructions.append('R')
                direction = LEFT
            # otherwise check if it can move right
            elif tile_right(tiles, pos) == '#':
                instructions.append('L')
                direction = RIGHT
            # otherwise reached end of input
            else:
                break

        elif direction == LEFT:
            counter = 0
            while tile_left(tiles, pos) == '#':
                counter += 1
                pos = (pos[0] - 1, pos[1])
                draw_tiles(tiles, pos)

            if counter:
                instructions.append(counter)

            # check if it can move up, if so, turn
            if tile_up(tiles, pos) == '#':
                instructions.append('R')
                direction = UP
            # otherwise check if it can move down
            elif tile_down(tiles, pos) == '#':
                instructions.append('L')
                direction = DOWN
            # otherwise reached end of harness
            else:
                break

        elif direction == RIGHT:
            counter = 0
            while tile_right(tiles, pos) == '#':
                counter += 1
                pos = (pos[0] + 1, pos[1])
                draw_tiles(tiles, pos)

            if counter:
                instructions.append(counter)

            # check if it can move up, if so, turn
            if tile_up(tiles, pos) == '#':
                instructions.append('L')
                direction = UP
            # otherwise check if it can move down
            elif tile_down(tiles, pos) == '#':
                instructions.append('R')
                direction = DOWN
            # otherwise reached end of harness
            else:
                break

    orig_instructions = deepcopy(instructions)
    # Find instructions subsets
    seqs = []
    for j in range(3):
        # overriding the max length here (part manual solution)
        for i in range(0, 11, 2):
            current = ''.join([str(x) for x in instructions[:i]])
            remainder = ''.join([str(x) for x in instructions[i:]])

            if current not in remainder:
                break

        seq = instructions[:i-2]
        seqs.append(seq)
        str_seq = ''.join([str(x).zfill(2) if i % 2 == 1 else f'|{x}' for i, x in enumerate(seq)])
        str_instructions = ''.join([str(x).zfill(2) if i % 2 == 1 else f'|{x}' for i, x in enumerate(instructions)])
        str_instructions = str_instructions.replace(str_seq, '')
        tuples = [(x[0], int(x[1:])) for x in str_instructions.split('|') if x]
        instructions = [x for sublist in tuples for x in sublist]

    orig_instructions = ''.join([str(x) for x in orig_instructions])
    seq_a = ''.join([str(x) for x in seqs[0]])
    seq_b = ''.join([str(x) for x in seqs[1]])
    seq_c = ''.join([str(x) for x in seqs[2]])
    main_routine = []
    while orig_instructions:
        if orig_instructions.startswith(seq_a):
            orig_instructions = orig_instructions[len(seq_a):]
            main_routine.append('A')
        elif orig_instructions.startswith(seq_b):
            orig_instructions = orig_instructions[len(seq_b):]
            main_routine.append('B')
        elif orig_instructions.startswith(seq_c):
            orig_instructions = orig_instructions[len(seq_c):]
            main_routine.append('C')

    input_sequence = [
        *','.join(main_routine), '\n',
        *','.join([str(x) for x in seqs[0]]), '\n',
        *','.join([str(x) for x in seqs[1]]), '\n',
        *','.join([str(x) for x in seqs[2]]), '\n',
    ]
    input_sequence.append('n')
    input_sequence.append('\n')

    inputs = deque(input_sequence)

    with open("17_input.txt","r") as file:
        lines = file.read().split('\n')[0]

    registers = [int(x) for x in lines.split(',')] + [0] * 10000
    # override the rover mode
    registers[0] = 2

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
            user_input = ord(inputs.popleft())

            registers[save_ix] = user_input
            index += 2
        elif opcode == OUTPUT_OP:
            left = get_operand(first_param_mode, index+1, registers, relative_base=relative_base)
            output.append(left)

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

