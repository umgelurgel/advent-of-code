
if __name__ == '__main__':
    total = 0
    with open("02_a_input.txt","r") as file:
        lines = file.read().split('\n')[0]

    registers = [int(x) for x in lines.split(',')]

    # print(registers)

    # replace the registers as requested
    registers[1] = 12
    registers[2] = 2

    ADD_OP = 1
    MULT_OP = 2
    BREAK_OP = 99

    index = 0
    while True:
        print(f'{index} out of {len(registers)}')
        print(registers)
        opcode = registers[index]

        if opcode == BREAK_OP:
            print('break opcode found')
            break
        elif opcode == ADD_OP:
            left_ix = registers[index + 1]
            right_ix = registers[index + 2]
            target_ix = registers[index + 3]

            registers[target_ix] = registers[left_ix] + registers[right_ix]
        elif opcode == MULT_OP:
            left_ix = registers[index + 1]
            right_ix = registers[index + 2]
            target_ix = registers[index + 3]

            registers[target_ix] = registers[left_ix] * registers[right_ix]
        else:
            print('error!')
            break

        index += 4

    print('program terminated')
