from collections import deque, Counter


if __name__ == '__main__':
    with open("input.txt", "r") as file:
    # with open("test_input.txt", "r") as file:
        # Remove empty lines
        lines = [line for line in file.read().split('\n') if line]

    grid = []
    # Instantiate grid adding padding at all sides to make the grid evolution simpler.
    grid.append(['$'] * (2 + len(lines[0])))
    for line in lines:
        grid.append(['$', *line, '$'])
    grid.append(['$'] * (2 + len(lines[0])))

    def print_grid():
        for line in grid:
            print(''.join(line))

    max_iter = 10
    for i in range(max_iter):
        # print(f'Iteration: {i}')
        # print_grid()
        # # input()

        new_grid = []
        new_grid.append(grid[0])
        for y_ix in range(1, len(grid) - 1):
            current_row = ['$']
            for x_ix in range(1, len(grid[y_ix]) - 1):
                neighbours = Counter([
                    *grid[y_ix - 1][x_ix - 1: x_ix + 2],
                    grid[y_ix][x_ix - 1],
                    grid[y_ix][x_ix + 1],
                    *grid[y_ix + 1][x_ix - 1: x_ix + 2],
                ])

                cur_symbol = grid[y_ix][x_ix]
                if cur_symbol == '.' and neighbours['|'] >= 3:
                    cur_symbol = '|'
                elif cur_symbol == '|' and neighbours['#'] >= 3:
                    cur_symbol = '#'
                elif cur_symbol == '#':
                    if neighbours['#'] >= 1 and neighbours['|'] >= 1:
                        cur_symbol = '#'
                    else:
                        cur_symbol = '.'
                current_row.append(cur_symbol)

            current_row.append('$')
            new_grid.append(current_row)

        new_grid.append(grid[-1])
        grid = new_grid

    final_count = Counter([char for sublist in grid for char in sublist])
    print(final_count)
    final_score = final_count['#'] * final_count['|']
    print(f'Final score is: {final_score}')