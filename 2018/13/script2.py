from datetime import datetime

if __name__ == '__main__':
    with open("input.txt", "r") as file:
    # with open("test_input2.txt", "r") as file:
        # Remove empty lines
        lines = [line for line in file.read().split('\n') if line]

    carts = []
    # Find carts and directions
    cart_symbols = ['<', '^', '>', 'v']
    cart_id = 0
    for y_ix in range(len(lines)):
        for x_ix in range(len(lines[y_ix])):
            if lines[y_ix][x_ix] in cart_symbols:
                dir = cart_symbols.index(lines[y_ix][x_ix])
                new_cart = {
                    'x': x_ix,
                    'y': y_ix,
                    'dir': dir,
                    # cart turns: 0 - left, 1-straight, 2-right
                    'turn': 0,
                    'last_pos': ('|' if dir % 2 == 1 else '-'),
                    'cart_id': cart_id,
                }
                cart_id += 1
                carts.append(new_cart)

    # Create a mutable grid
    grid = []
    for line in lines:
        grid.append(list(line))

    counter = 0
    crashed_carts = set()
    while True:
        counter += 1
        # for line in grid:
        #     print(''.join(line))
        # input()

        # Order carts in the order they'll be moving.
        carts.sort(key=lambda cart: 1000 * cart['y'] + cart['x'])

        if len(carts) - len(crashed_carts) == 1:
            last_cart = [cart for cart in carts if cart['cart_id'] not in crashed_carts][0]
            print(f'The final position is: {last_cart["x"]},{last_cart["y"]}')
            exit()

        new_carts = []
        for cart in carts:
            # Check if the cart hasn't crashed
            cart_id = cart['cart_id']
            if cart_id in crashed_carts:
                crashed_carts.remove(cart_id)
                grid[cart['y']][cart['x']] = cart['last_pos']
                continue

            # Calculate new cart position
            new_x = cart['x']
            new_y = cart['y']
            dir = cart['dir']
            if dir == 0:
                new_x -= 1
            elif dir == 1:
                new_y -= 1
            elif dir == 2:
                new_x += 1
            elif dir == 3:
                new_y += 1

            # Calculate new direction if needed
            target_pos = grid[new_y][new_x]
            turn = cart['turn']
            # ['<', '^', '>', 'v']
            if target_pos == '/':
                if dir == 0:
                    dir = 3
                elif dir == 1:
                    dir = 2
                elif dir == 2:
                    dir = 1
                elif dir == 3:
                    dir = 0
            elif target_pos == '\\':
                if dir == 0:
                    dir = 1
                elif dir == 1:
                    dir = 0
                elif dir == 2:
                    dir = 3
                elif dir == 3:
                    dir = 2
            elif target_pos == '+':
                if turn == 0:
                    dir = (dir - 1) % 4
                elif turn == 2:
                    dir = (dir + 1) % 4

                turn = (turn + 1) % 3

            if target_pos in cart_symbols:
                # Crash, remove both carts from the grid.
                print(f'{counter}: Crash at {new_x},{new_y}')
                # Current cart won't be added to new carts so it's removed.
                # Need to update the grid
                grid[cart['y']][cart['x']] = cart['last_pos']

                # Remove the other cart:
                current_carts = [x for x in carts if x['x'] == new_x and x['y'] == new_y]
                if len(current_carts) == 0:
                    current_cart = [x for x in new_carts if x['x'] == new_x and x['y'] == new_y][0]
                else:
                    current_cart = current_carts[0]

                crashed_carts.add(current_cart['cart_id'])

            else:
                # Update the grid
                grid[cart['y']][cart['x']] = cart['last_pos']
                last_pos = grid[new_y][new_x]
                grid[new_y][new_x] = cart_symbols[dir]

                # Save the cart changes
                new_carts.append({
                    'x': new_x,
                    'y': new_y,
                    'dir': dir,
                    'turn': turn,
                    'last_pos': last_pos,
                    'cart_id': cart['cart_id'],
                })

        carts = new_carts


