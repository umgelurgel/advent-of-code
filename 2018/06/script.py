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
            min_loc_id = -1
            min_loc_distance = max_x + max_y

            for loc_id, loc_coords in locs.items():
                distance = abs(x - loc_coords['x']) + abs(y - loc_coords['y'])
                if distance == min_loc_distance:
                    min_loc_id = -1
                elif distance < min_loc_distance:
                    min_loc_id = loc_id
                    min_loc_distance = distance

            grid[x][y] = min_loc_id

    # Find the locations that have infite grids
    top = set(grid[0])
    bottom = set(grid[-1])
    left = set([subgrid[0] for subgrid in grid])
    right = set([subgrid[-1] for subgrid in grid])
    infinite_grids = top.union(bottom).union(left).union(right)

    flat_grid = [item for sublist in grid for item in sublist]
    counted = Counter(flat_grid)
    for loc_id in infinite_grids:
        del counted[loc_id]

    print(f'Largest finite area i: {max(counted.values())}')
