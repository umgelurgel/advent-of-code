
if __name__ == '__main__':
    filename = "03_a_input.txt"
    # filename = "03_test_input.txt"

    with open(filename,"r") as file:
        lines = file.read().split('\n')

    # remove empty lines
    lines = [line for line in lines if line]
    print(lines)

    def generate_wire(line):
        wire = []
        wire_distances = {}
        cur_ix = (0,0)
        step_count = 1
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
                if cur_ix not in wire_distances:
                    wire_distances[cur_ix] = step_count
                step_count += 1
                wire.append(cur_ix)

        return wire, wire_distances

    wire_0, distances_0 = generate_wire(lines[0])
    wire_1, distances_1 = generate_wire(lines[1])

    intersections = set(wire_0) & set(wire_1)
    def step_distance(point):
        return distances_0[point] + distances_1[point]

    lowest_distance = min(step_distance(elem) for elem in intersections)
    print(f'lowest distance: {lowest_distance}')
