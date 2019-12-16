import random

if __name__ == '__main__':
    with open("16_input.txt","r") as file:
        lines = file.read().split('\n')[0]

    base_pattern = [0, 1, 0, -1]

    numbers = [int(x) for x in list(lines)] * 10_000
    offset = int(''.join([str(x) for x in numbers[:7]]))
    numbers = numbers[offset:]
    phase = 0

    # Taken from https://github.com/mebeim/aoc/blob/master/2019/README.md#day-16---flawed-frequency-transmission
    while phase < 100:
        for i in range(len(numbers) - 2, -1, -1):
            numbers[i] += numbers[i + 1]
            numbers[i] %= 10

        phase += 1
        print(f'{phase}: {"".join([str(x) for x in numbers[:8]])}')
