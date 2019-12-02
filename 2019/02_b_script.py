from copy import deepcopy
if __name__ == '__main__':
    total = 0
    with open("02_a_input.txt","r") as file:
        lines = file.read().split('\n')[0]

    original_registers = [int(x) for x in lines.split(',')]

    # print(registers)

    ADD_OP = 1
    MULT_OP = 2
    BREAK_OP = 99

    target_value = 19690720
    noun = 0
    verb = 0

    while True:
        print(f'running for: noun {noun} and verb {verb}')
        registers = deepcopy(original_registers)
        registers[1] = noun
        registers[2] = verb
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

        if registers[0] == target_value:
            print(f'success: the noun is {noun} and verb is {verb}')
            print(f'the answer is {noun * 100 + verb}')
            break
        else:
            noun += 1
            if noun == 100:
                noun = 0
                verb += 1

    print('program terminated')
