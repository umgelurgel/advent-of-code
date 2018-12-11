import re
from datetime import datetime

from blist import blist

if __name__ == '__main__':
    x_size = 300
    y_size = 300
    grid_no = 3463

    grid = blist([[0] * x_size for _ in range(y_size)])

    def power(x, y, grid_no=grid_no):
        rack_id = x + 10
        power_level = ((rack_id * y + grid_no) * rack_id) % 1000 // 100 - 5
        return power_level

    for y_ix in range(len(grid)):
        for x_ix in range(len(grid[y_ix])):
            grid[y_ix][x_ix] = power(x=x_ix + 1, y=y_ix + 1)

    power_cells = blist([[0] * (x_size) for _ in range(y_size)])

    max_cell_pow = 0
    max_cell_x = -1
    max_cell_y = -1
    max_cell_size = -1

    for y_ix in range(len(power_cells)):
        print(f'{datetime.now()}: {y_ix}')
        for x_ix in range(len(power_cells[y_ix])):
            for size in range(min([y_size - y_ix + 1, x_size - x_ix + 1])):
                cell_power = sum([sum(grid[y_ix + i][x_ix:x_ix + size]) for i in range(size)])

                if cell_power > max_cell_pow:
                    max_cell_pow = cell_power
                    max_cell_x = x_ix + 1
                    max_cell_y = y_ix + 1
                    max_cell_size = size

    print(f'The coordinates of the largest cell are: {max_cell_x},{max_cell_y},{max_cell_size}')