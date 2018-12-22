from datetime import datetime


if __name__ == '__main__':
    with open("input.txt", "r") as file:
    # with open("test_input.txt", "r") as file:
        # Remove empty lines
        lines = [line for line in file.read().split('\n') if line]

    regs = [0] * 6

    def addr(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], regs[arg1] + regs[arg2], *regs[out_reg_id + 1:]]
    def addi(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], regs[arg1] + arg2, *regs[out_reg_id + 1:]]

    def mulr(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], regs[arg1] * regs[arg2], *regs[out_reg_id + 1:]]
    def muli(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], regs[arg1] * arg2, *regs[out_reg_id + 1:]]

    def banr(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], regs[arg1] & regs[arg2], *regs[out_reg_id + 1:]]
    def bani(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], regs[arg1] & arg2, *regs[out_reg_id + 1:]]

    def borr(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], regs[arg1] | regs[arg2], *regs[out_reg_id + 1:]]
    def bori(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], regs[arg1] | arg2, *regs[out_reg_id + 1:]]

    def setr(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], regs[arg1], *regs[out_reg_id + 1:]]
    def seti(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], arg1, *regs[out_reg_id + 1:]]

    def gtir(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], 1 if arg1 > regs[arg2] else 0, *regs[out_reg_id + 1:]]
    def gtri(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], 1 if regs[arg1] > arg2 else 0, *regs[out_reg_id + 1:]]
    def gtrr(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], 1 if regs[arg1] > regs[arg2] else 0, *regs[out_reg_id + 1:]]

    def eqir(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], 1 if arg1 == regs[arg2] else 0, *regs[out_reg_id + 1:]]
    def eqri(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], 1 if regs[arg1] == arg2 else 0, *regs[out_reg_id + 1:]]
    def eqrr(regs, arg1, arg2, out_reg_id): return [*regs[0:out_reg_id], 1 if regs[arg1] == regs[arg2] else 0, *regs[out_reg_id + 1:]]

    # Set instructin pointer
    inst_p = int(lines[0].replace('#ip ', ''))

    instructions = []
    for line in lines[1:]:
        split_line = line.split()
        func = split_line[0]
        args = [int(x) for x in split_line[1:]]
        instructions.append((func, args))

    counter = 0
    while True:
        try:
            if counter % 10000 == 0:
                print(f'{datetime.now()}: {counter}')
            counter += 1
            # print(regs[inst_p])
            # print(regs)
            # input()

            inst = instructions[regs[inst_p]]
        except IndexError:
            break

        func_name = inst[0]
        args = inst[1]
        # print(f'{func_name}: {args}')
        regs = eval(f'{func_name}{regs, args[0], args[1], args[2]}')

        regs[inst_p] += 1

    print(regs[0])