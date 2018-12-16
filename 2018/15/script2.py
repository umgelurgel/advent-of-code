from collections import deque
from datetime import datetime

if __name__ == '__main__':
    # with open("input.txt", "r") as file:
    # with open("test_input.txt", "r") as file:
    # with open("test_input2.txt", "r") as file:
    # with open("reddit_input3.txt", "r") as file:
    with open("input.txt", "r") as file:
        # Remove empty lines
        lines = [line for line in file.read().split('\n') if line]

    # Create a mutable grid
    grid = []
    for line in lines:
        grid.append(list(line))

    characters = {}
    # Via trial and error
    elf_attack = 34
    # Find all characters on the grid
    for y_ix in range(len(grid)):
        for x_ix in range(len(grid[y_ix])):
            cur_symbol = grid[y_ix][x_ix]
            if cur_symbol in {'E', 'G'}:
                characters[len(characters)] = {
                    'type': cur_symbol,
                    'health': 200,
                    'x': x_ix,
                    'y': y_ix,
                    'attack': 3 if cur_symbol == 'G' else elf_attack
                }

    turn_counter = 0
    while True:
        # Order characters in the order they'll be acting.
        temp_sorted_chars = sorted(list(characters.values()), key=lambda char: 1000 * char['y'] + char['x'])
        characters = {}
        for i, temp_char in enumerate(temp_sorted_chars):
            characters[i] = temp_char

        print(f'Turn {turn_counter} state:')
        for grid_line in grid:
            print(''.join(grid_line))
        for char in characters.values():
            print(f"{char['type']} ({char['x']},{char['y']}): {char['health']}")
        print()
        # input()

        for char_id in characters.keys():
            character = characters[char_id]
            # Skip dead characters
            if character['health'] <= 0:
                continue

            x_pos = character['x']
            y_pos = character['y']
            enemy_symbol = 'G' if character['type'] == 'E' else 'E'

            # Check if the unit can attack
            positions = [
                (y_pos - 1, x_pos),
                (y_pos, x_pos - 1),
                (y_pos, x_pos + 1),
                (y_pos + 1, x_pos),
            ]
            adjacent_enemies = []
            for y_near, x_near in positions:
                if grid[y_near][x_near] == enemy_symbol:
                    # Check if the character is alive, if so attack, and break out of the loop
                    enemy_char_id, enemy_char = [
                        (x_id, x) for x_id, x in characters.items() if x['x'] == x_near and x['y'] == y_near
                    ][0]
                    if enemy_char['health'] > 0:
                        adjacent_enemies.append({**enemy_char, 'id':enemy_char_id})

            if adjacent_enemies:
                # Find the enemy with the lowest hit points:
                adjacent_enemies.sort(key=lambda enemy: 10000 * enemy['health'] + 100 * enemy['y'] + enemy['x'])
                # Attack
                target_enemy = adjacent_enemies[0]

                target_enemy['health'] -= character['attack']
                characters[target_enemy['id']] = target_enemy

                # If the enemy died, remove them from the grid to not confuse the pathfinding algorith,.
                if target_enemy['health'] <= 0:
                    if target_enemy['type'] == 'E':
                        print('an elf died')
                        exit()
                    grid[target_enemy['y']][target_enemy['x']] = '.'

                # If this character attacked, it doesn't take further action this turn.
                continue

            # If the character didn't attack, find the closest enemy.
            positions = [
                (y_pos + 1, x_pos),
                (y_pos, x_pos + 1),
                (y_pos, x_pos - 1),
                (y_pos - 1, x_pos),
            ]
            distances = {
                (y_pos, x_pos): 0,
                (y_pos - 1, x_pos): 1,
                (y_pos, x_pos - 1): 1,
                (y_pos, x_pos + 1): 1,
                (y_pos + 1, x_pos): 1,
            }
            back_steps = {}
            enemies = []
            while True:
                next_positions = []
                while positions:
                    y_next, x_next = positions.pop()
                    distance = distances[(y_next, x_next)]
                    symbol_next = grid[y_next][x_next]

                    # Check if it's an enemy, if so, add them to enemy list.
                    if symbol_next == enemy_symbol:
                        enemies.append((y_next, x_next, distance))

                    # Check if it's an empty position, and if so, add all new adjances positions to next_positions
                    elif symbol_next == '.':
                        pos_candidates = [
                            (y_next - 1, x_next),
                            (y_next, x_next - 1),
                            (y_next, x_next + 1),
                            (y_next + 1, x_next),
                        ]
                        for y_cand, x_cand in pos_candidates:
                            symbol_cand = grid[y_cand][x_cand]
                            if (y_cand, x_cand) not in distances.keys() and symbol_cand not in {'#', character['type']}:
                                next_positions.append((y_cand, x_cand))
                                distances[(y_cand, x_cand)] = distance + 1
                                back_steps[(y_cand, x_cand)] = (y_next, x_next)

                # If enemies have been found in this iteration, those are the closest enemies to
                if enemies or not next_positions:
                    break
                else:
                    positions = next_positions
                    positions.reverse()

            if enemies:
                # One or more enemies have been found - find the closest and the path to them.
                enemies.sort(key=lambda enemy: 10000 * enemy[2] + 100 * enemy[0] + enemy[1])
                closest = enemies[0]

                # Step back the closest path to enemy
                step = (closest[0], closest[1])
                while step in back_steps:
                    step = back_steps[step]

                # Move the character by a step
                characters[char_id] = {
                    **character,
                    'y': step[0],
                    'x': step[1],
                }

                # Update the grid
                grid[y_pos][x_pos] = '.'
                grid[step[0]][step[1]] = character['type']

                # Once a unit has moved, it can attack
                y_pos = step[0]
                x_pos = step[1]
                positions = [
                    (y_pos - 1, x_pos),
                    (y_pos, x_pos - 1),
                    (y_pos, x_pos + 1),
                    (y_pos + 1, x_pos),
                ]
                adjacent_enemies = []
                for y_near, x_near in positions:
                    if grid[y_near][x_near] == enemy_symbol:
                        # Check if the character is alive, if so attack, and break out of the loop
                        enemy_char_id, enemy_char = [
                            (x_id, x) for x_id, x in characters.items() if x['x'] == x_near and x['y'] == y_near
                        ][0]
                        if enemy_char['health'] > 0:
                            adjacent_enemies.append({**enemy_char, 'id':enemy_char_id})

                if adjacent_enemies:
                    # Find the enemy with the lowest hit points:
                    adjacent_enemies.sort(key=lambda enemy: 10000 * enemy['health'] + 100 * enemy['y'] + enemy['x'])
                    # Attack
                    target_enemy = adjacent_enemies[0]

                    target_enemy['health'] -= character['attack']
                    characters[target_enemy['id']] = target_enemy

                    # If the enemy died, remove them from the grid to not confuse the pathfinding algorith,.
                    if target_enemy['health'] <= 0:
                        if target_enemy['type'] == 'E':
                            print('an elf died')
                            exit()
                        grid[target_enemy['y']][target_enemy['x']] = '.'

                    # If this character attacked, it doesn't take further action this turn.
                    continue

        # Remove dead characters
        characters = {char_id: char for char_id, char in characters.items() if char['health'] > 0}

        # Check if only characters of a single type prevail, if so, end game.
        char_types = {x['type'] for x in characters.values()}
        if len(char_types) == 1:
            print(f'Game over in turn: {turn_counter}')
            healths = [x['health'] for x in characters.values()]
            print(f'Game result is: {sum(healths) * turn_counter} or {sum(healths) * (turn_counter + 1)}')
            exit()
        else:
            turn_counter += 1

