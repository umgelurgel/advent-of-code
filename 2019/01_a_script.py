
if __name__ == '__main__':
    total = 0
    with open("01_a_input.txt","r") as file:
        lines = file.read().split('\n')

    # print(lines)

    total = 0

    for line in lines:
        if not line:
            continue

        fuel = int(int(line) / 3) - 2
        total += fuel

    print(f'Total fuel requires is {total}')