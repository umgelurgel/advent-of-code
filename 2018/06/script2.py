import math
from collections import defaultdict, Counter


if __name__ == '__main__':
    with open("input.txt", "r") as file:
        # Remove empty lines
        lines = [line for line in file.read().split('\n') if line]

    locs = defaultdict(dict)
    for i, line in enumerate(lines):
        x, y = line.replace(' ', '').split(',')
        locs[i]['x'] = int(x)
        locs[i]['y'] = int(y)

    x_locs = [loc['x'] for loc in locs.values()]
    y_locs = [loc['y'] for loc in locs.values()]
    max_x = max(x_locs)
    max_y = max(y_locs)

    grid = [[-1] * (max_y + 1) for i in range(max_x + 1)]
    for loc_id, loc_coords in locs.items():
        grid[loc_coords['x']][loc_coords['y']] = loc_id

    # Annotate the grid with the closest location
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            distance_sum = sum(abs(x - loc['x']) + abs(y - loc['y']) for loc in locs.values())

            if distance_sum < 10000:
                grid[x][y] = '#'

    flat_grid = [item for sublist in grid for item in sublist]
    counted = Counter(flat_grid)

    print(f'Safe area size is: {counted["#"]}')
