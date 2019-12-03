
if __name__ == '__main__':
    filename = "03_a_input.txt"
    # filename = "03_test_input.txt"

    with open(filename,"r") as file:
        lines = file.read().split('\n')

    # remove empty lines
    lines = [line for line in lines if line]
    print(lines)

    wires = []
    for line in lines:
        wire = []
        cur_ix = (0,0)
        for instruction in line.split(','):
            direction = instruction[0]
            length = int(instruction[1:])

            if direction == 'U':
                increment = lambda x: (x[0], x[1] + 1)
            if direction == 'D':
                increment = lambda x: (x[0], x[1] - 1)
            if direction == 'L':
                increment = lambda x: (x[0] - 1, x[1])
            if direction == 'R':
                increment = lambda x: (x[0] + 1, x[1])

            for i in range(length):
                cur_ix = increment(cur_ix)
                wire.append(cur_ix)

        wires.append(wire)

    intersections = set(wires[0]) & set(wires[1])
    def manhattan_distance(point):
        return abs(point[0]) + abs(point[1])

    lowest_distance = min(manhattan_distance(elem) for elem in intersections)
    print(f'lowest distance: {lowest_distance}')

    print('program terminated')
