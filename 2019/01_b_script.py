
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

        extra_fuel_weight = fuel
        while True:
            extra_fuel_required = int(extra_fuel_weight / 3) - 2

            if extra_fuel_required <= 0:
                break
            else:
                total += extra_fuel_required
                extra_fuel_weight = extra_fuel_required

    print(f'Total fuel required is {total}')