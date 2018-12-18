from collections import deque, Counter


if __name__ == '__main__':
    with open("input.txt", "r") as file:
    # with open("test_input.txt", "r") as file:
    # with open("test_input2.txt", "r") as file:
    # Remove empty lines
        lines = [line for line in file.read().split('\n') if line]

    # stores clay coordinates: x_min, x_max, y_min, y_max
    clay_lines = []
    for line in lines:
        if line.startswith('x'):
            clay_coords = [int(x) for x in line.replace('x=', '').replace(' y=', '').replace('..',',').split(',')]
            clay_coords = [clay_coords[0], *clay_coords]
        elif line.startswith('y'):
            clay_coords = [int(x) for x in line.replace('y=', '').replace(' x=', '').replace('..',',').split(',')]
            clay_coords = [clay_coords[1], clay_coords[2], clay_coords[0], clay_coords[0]]
        else:
            print('error parsing clay data')
            exit(-1)

        clay_lines.append(clay_coords)

    # Find the size of the grid
    x_max = max(max(x[0] for x in clay_lines), max(x[1] for x in clay_lines)) + 1
    x_min = min(min(x[0] for x in clay_lines), min(x[1] for x in clay_lines))
    y_max = max(max(y[2] for y in clay_lines), max(y[3] for y in clay_lines))
    y_min = min(min(y[2] for y in clay_lines), min(y[3] for y in clay_lines))

    grid = [['.'] * (x_max + 2) for _ in range(y_max + 1)]
    grid[0][500] = '*'

    def print_grid():
        for y_ix in range(len(grid)):
            print(''.join(grid[y_ix][x_min - 1:]))

    # Draw the clay
    for clay_x_min, clay_x_max, clay_y_min, clay_y_max in clay_lines:
        for y_ix in range(clay_y_min, clay_y_max + 1):
            for x_ix in range(clay_x_min, clay_x_max + 1):
                grid[y_ix][x_ix] = '#'

    # Mark containers that could hold water without spilling
    for y_ix in range(len(grid) - 1, -1, -1):
        row = ''.join(grid[y_ix])

        x_start = row.find('#')
        x_end = row.find('.', x_start)
        while x_start != -1 and x_end != -1:
            y_offset = 1
            while True:
                y_new = y_ix - y_offset

                if grid[y_new][x_start] == '#' and grid[y_new][x_end - 1] == '#':
                    for x_new in range(x_start + 1, x_end):
                        if grid[y_new][x_new] == '.':
                            grid[y_new][x_new] = '@'

                    y_offset += 1
                elif grid[y_new][x_start] == '#':
                    iter_row = ''.join(grid[y_new])
                    next_wall_ix = iter_row.find('#', x_start + 1)
                    if next_wall_ix < x_end:
                        for x_new in range(x_start + 1, next_wall_ix):
                            if grid[y_new][x_new] == '.':
                                grid[y_new][x_new] = '@'
                    break
                elif grid[y_new][x_end - 1] == '#':
                    iter_row = ''.join(grid[y_new])
                    prev_wall_ix = iter_row.rfind('#', x_start + 1, x_end - 1)
                    if prev_wall_ix != -1:
                        for x_new in range(prev_wall_ix + 1, x_end):
                            if grid[y_new][x_new] == '.':
                                grid[y_new][x_new] = '@'
                    break
                else:
                    break

            x_start = row.find('#', x_start + 1)
            possible_ends = [x for x in [
                row.find('.', x_start),
                row.find('@', x_start),
            ] if x != -1]
            if possible_ends:
                x_end = min(possible_ends)
            else:
                x_end = -1


    steps = deque([(500, 0)])
    water = {
        '.': '|',
        '@': '~',
    }
    while len(steps):
        # print_grid()
        # input()

        x_ix, y_ix = steps[-1]
        y_down = y_ix + 1
        x_left = x_ix - 1
        x_right = x_ix + 1
        if y_down <= y_max and grid[y_down][x_ix] in {'.', '@'}:
            grid[y_down][x_ix] = water[grid[y_down][x_ix]]
            steps.append((x_ix, y_down))

        elif y_down == y_max + 1:
            steps.pop()

        elif x_left >= 0 and grid[y_ix][x_left] in {'.', '@'} and grid[y_down][x_ix] != '|':
            grid[y_ix][x_left] = water[grid[y_ix][x_left]]
            steps.append((x_left, y_ix))
        elif x_right <= x_max and grid[y_ix][x_right] in {'.', '@'} and grid[y_down][x_ix] != '|':
            grid[y_ix][x_right] = water[grid[y_ix][x_right]]
            steps.append((x_right, y_ix))
        else:
            steps.pop()

    # print_grid()
    final_count = Counter([char for sublist in grid[y_min:] for char in sublist])
    print(final_count)
    final_score = final_count['~'] + final_count['|']
    print(f'Final score is: {final_score}')