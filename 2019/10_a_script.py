from collections import deque
from copy import deepcopy
from math import gcd

if __name__ == '__main__':
    with open("10_input_test.txt","r") as file:
        lines = [line for line in file.read().split('\n') if line]

    # get a list of all asteroids
    asteroids = deque()
    for j in range(len(lines)):
        for i in range(len(lines[j])):
            if lines[j][i] == '#':
                asteroids.append((i, j))

    max_x = len(lines[0])
    max_y = len(lines)
    grid_size =  max_x * max_y


    def manhattan_distance(first, second):
        return abs(first[0]-second[0]) + abs(first[1]-second[1])


    max_seen = 0
    best_coordinates = None

    # for each asteroid
    while asteroids:
        ast_x, ast_y = asteroids.popleft()
        print(f'Processing asteroid {ast_x, ast_y}')

        grid = []
        for j in range(len(lines)):
            grid.append(list(lines[j]))

        visited = {(ast_x, ast_y)}
        last_processed = [(ast_x, ast_y)]
        seen = []
        # if not all points visited
        while len(visited) < grid_size:
            # gets points 1 distance away from the ones checked last
            # print(f'Finding neighbours of {last_processed}')
            # print(f'already visited: {visited}')
            to_process = deque()
            for point in last_processed:
                for j in range(len(grid)):
                    for i in range(len(grid[j])):
                        if (i,j) not in visited and manhattan_distance((i,j), point) == 1:
                            to_process.append((i,j))
                            visited.add((i,j))

            # print(f'Neighbours are {to_process}')
            last_processed = []
            while to_process:
                cur_x, cur_y = to_process.popleft()

                # add to processed list
                last_processed.append((cur_x, cur_y))

                if grid[cur_y][cur_x] == '.':
                    continue

                # if they're an asteroid, update visible world map
                seen.append((cur_x, cur_y))
                vec_x = cur_x - ast_x
                vec_y = cur_y - ast_y
                ratio = gcd(vec_x, vec_y)
                vec_x = int(vec_x/ratio)
                vec_y = int(vec_y/ratio)

                next_x = cur_x + vec_x
                next_y = cur_y + vec_y


                while next_x >=0 and next_x < max_x and next_y >= 0 and next_y < max_y:
                    # print(f'updating: {next_x} {next_y}')
                    grid[next_y][next_x] = '.'
                    next_x = next_x + vec_x
                    next_y = next_y + vec_y

        # if all points visited, compare number of asteroids seen
        print(f'asteroid {ast_x}, {ast_y} sees {len(seen)}')
        if len(seen) > max_seen:
            max_seen = len(seen)
            best_coordinates = (ast_x, ast_y)

    print(f'Best position is {ast_x}, {ast_y} with visibility of {max_seen}')
