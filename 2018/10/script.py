import re

if __name__ == '__main__':
    with open("input.txt", "r") as file:
        # Remove empty lines
        lines = [line for line in file.read().split('\n') if line]

    regex_str = r'^position=<([ -]\d+), ([ -]\d+)> velocity=<([ -]\d+), ([ -]\d+)>'
    regex = re.compile(regex_str)

    loc_x = []
    loc_y = []
    vel_x = []
    vel_y = []

    for line in lines:
        match = regex.match(line)
        pos_x, pos_y, delta_x, delta_y = [int(x) for x in match.groups()]
        loc_x.append(pos_x)
        loc_y.append(pos_y)
        vel_x.append(delta_x)
        vel_y.append(delta_y)

    range_x = abs(max(loc_x) - min(loc_x))
    range_y = abs(max(loc_y) - min(loc_y))

    def print_message():
        print('\n\n\n')
        x_offset = min(loc_x)
        y_offset = min(loc_y)
        grid = [['.'] * (max(loc_x) + 1 - x_offset) for _ in range(max(loc_y) + 1 - y_offset)]

        for i in range(len(loc_x)):
            grid[loc_y[i] - y_offset][loc_x[i] - x_offset] = '#'

        for grid_line in grid:
            print(''.join(grid_line))

    counter = 0
    while True:
        for i in range(len(loc_x)):
            loc_x[i] += vel_x[i]
            loc_y[i] += vel_y[i]

        new_range_x = abs(max(loc_x) - min(loc_x))
        new_range_y = abs(max(loc_y) - min(loc_y))

        if new_range_x < 100:
            print_message()

        if new_range_x > range_x and new_range_y > range_y:
            break
        else:
            range_x = new_range_x
            range_y = new_range_y
            counter += 1

    print(f'The delay is {counter}')
