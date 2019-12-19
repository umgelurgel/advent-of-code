from collections import deque
from copy import deepcopy

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

dirname = {
    UP: 'UP',
    RIGHT: 'RIGHT',
    LEFT: 'LEFT',
    DOWN: 'DOWN',
}

class State:

    def __init__(self, pos, direction, step, keys, doors):
        self.pos = pos
        self.direction = direction
        self.step = step
        self.keys = set(keys)
        self.doors = set(doors)

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.step} going {dirname[self.direction]} from {self.pos}, {self.keys}, {self.doors}'

    def move(self, tiles, direction):
        if direction == RIGHT:
            pos = (self.pos[0] + 1, self.pos[1])
        elif direction == LEFT:
            pos = (self.pos[0] - 1, self.pos[1])
        elif direction == UP:
            pos = (self.pos[0], self.pos[1] - 1)
        elif direction == DOWN:
            pos = (self.pos[0], self.pos[1] + 1)

        target_tile = tiles[pos[1]][pos[0]]
        keys = set(self.keys)
        if target_tile.islower():
            keys.add(target_tile)

        doors = set(self.doors)
        if target_tile.isupper():
            doors.add(target_tile)

        return State(
            pos=pos,
            direction=direction,
            step=self.step + 1,
            keys=keys,
            doors=doors,
        )

    def turn(self, direction):
        return State(
            pos=self.pos,
            direction=direction,
            step=self.step,
            keys=self.keys,
            doors=self.doors,
        )

    def should_turn_back(self, previous):
        return self.keys != previous.keys or self.doors != previous.doors

    def turn_back(self):
        return State(
            pos=self.pos,
            direction=(self.direction + 2) % 4,
            step=self.step,
            keys=self.keys,
            doors=self.doors,
        )



if __name__ == '__main__':
    with open("18_input.txt","r") as file:
        lines = [line for line in file.read().split('\n') if line]

    tiles = [list(line) for line in lines]
    all_keys = set()

    # find entrance
    for y in range(len(tiles)):
        for x in range(len(tiles[y])):
            if tiles[y][x] == '@':
                pos = (x, y)
                tiles[y][x] = '.'
            if tiles[y][x].islower():
                all_keys.add(tiles[y][x])

    def draw_tiles(tiles, pos):
        tiles = deepcopy(tiles)
        tiles[pos[1]][pos[0]] = 'D'
        print('\n'.join([''.join(x) for x in tiles]))

    def tile_up(tiles, pos):
        if pos[1] - 1 >= 0:
            return tiles[pos[1] - 1][pos[0]]

    def tile_down(tiles, pos):
        if pos[1] + 1 < len(tiles):
            return tiles[pos[1] + 1][pos[0]]

    def tile_left(tiles, pos):
        if pos[0] - 1 >= 0:
            return tiles[pos[1]][pos[0] - 1]

    def tile_right(tiles, pos):
        if pos[0] + 1 < len(tiles[pos[1]]):
            return tiles[pos[1]][pos[0] + 1]

    def can_go(state, tile):
        return tile == '.' or tile.islower() or tile.lower() in state.keys

    states = deque()
    # Seed the initial states
    if tile_up(tiles, pos) != '#':
        states.append(State(pos=pos, direction=UP, step=0, keys=set(), doors=set()))
    if tile_down(tiles, pos) != '#':
        states.append(State(pos=pos, direction=DOWN, step=0, keys=set(), doors=set()))
    if tile_left(tiles, pos) != '#':
        states.append(State(pos=pos, direction=LEFT, step=0, keys=set(), doors=set()))
    if tile_right(tiles, pos) != '#':
        states.append(State(pos=pos, direction=RIGHT, step=0, keys=set(), doors=set()))

    while states:
        print(len(states))
        # input()

        current = states.popleft()
        pos = current.pos
        if current.keys == all_keys:
            break

        # print(current)
        # if current.step >= 6:
        #     import ipdb; ipdb.set_trace()

        if current.direction == UP:
            # Check whether it's a junction to the left or right
            if can_go(state=current, tile=tile_up(tiles, pos)):
                move = current.move(tiles=tiles, direction=UP)
                states.append(move)

                # Should we branch here? Only branch if we moved to a non-empty field (key or door)
                if move.should_turn_back(previous=current):
                    states.append(move.turn_back())

            if can_go(state=current, tile=tile_left(tiles, pos)):
                move = current.move(tiles=tiles, direction=LEFT)
                states.append(move)

                if move.should_turn_back(previous=current):
                    states.append(move.turn_back())
            if can_go(state=current, tile=tile_right(tiles, pos)):
                move = current.move(tiles=tiles, direction=RIGHT)
                states.append(move)

                if move.should_turn_back(previous=current):
                    states.append(move.turn_back())

        elif current.direction == LEFT:
            if can_go(state=current, tile=tile_left(tiles, pos)):
                move = current.move(tiles=tiles, direction=LEFT)
                states.append(move)

                # Should we branch here? Only branch if we moved to a non-empty field (key or door)
                if move.should_turn_back(previous=current):
                    states.append(move.turn_back())

            if can_go(state=current, tile=tile_up(tiles, pos)):
                move = current.move(tiles=tiles, direction=UP)
                states.append(move)

                if move.should_turn_back(previous=current):
                    states.append(move.turn_back())
            if can_go(state=current, tile=tile_down(tiles, pos)):
                move = current.move(tiles=tiles, direction=DOWN)
                states.append(move)

                if move.should_turn_back(previous=current):
                    states.append(move.turn_back())

        elif current.direction == RIGHT:
            if can_go(state=current, tile=tile_right(tiles, pos)):
                move = current.move(tiles=tiles, direction=RIGHT)
                states.append(move)

                # Should we branch here? Only branch if we moved to a non-empty field (key or door)
                if move.should_turn_back(previous=current):
                    states.append(move.turn_back())

            if can_go(state=current, tile=tile_up(tiles, pos)):
                move = current.move(tiles=tiles, direction=UP)
                states.append(move)

                if move.should_turn_back(previous=current):
                    states.append(move.turn_back())
            if can_go(state=current, tile=tile_down(tiles, pos)):
                move = current.move(tiles=tiles, direction=DOWN)
                states.append(move)

                if move.should_turn_back(previous=current):
                    states.append(move.turn_back())

        elif current.direction == DOWN:
            if can_go(state=current, tile=tile_down(tiles, pos)):
                move = current.move(tiles=tiles, direction=DOWN)
                states.append(move)

                # Should we branch here? Only branch if we moved to a non-empty field (key or door)
                if move.should_turn_back(previous=current):
                    states.append(move.turn_back())

            if can_go(state=current, tile=tile_left(tiles, pos)):
                move = current.move(tiles=tiles, direction=LEFT)
                states.append(move)

                if move.should_turn_back(previous=current):
                    states.append(move.turn_back())
            if can_go(state=current, tile=tile_right(tiles, pos)):
                move = current.move(tiles=tiles, direction=RIGHT)
                states.append(move)

                if move.should_turn_back(previous=current):
                    states.append(move.turn_back())


    print(f'Shortest path is {current.step} steps')
