import datetime

from numpy import lcm

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise Exception

        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    @property
    def energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def __repr__(self):
        return f'<{self.__class__.__name__} x={self.x}, y={self.y}, z={self.z}>'


if __name__ == '__main__':
    with open("12_input.txt","r") as file:
        lines = [line for line in file.read().split('\n') if line]

    positions = []
    velocities = []

    # initiate the system
    for line in lines:
        inputs = line.replace('<', '').replace('>', '').split(',')
        params = {}
        for i in inputs:
            key, value = i.split('=')
            params[key.strip()] = int(value)

        positions.append(Vector(**params))
        velocities.append(Vector(0,0,0))

    def velocity_update(left, right):
        if left < right:
            return 1
        elif left > right:
            return -1
        else:
            return 0

    def axis_hash(positions, velocities, axis):
        state = ''
        if axis == 0:
            attr_name = 'x'
        if axis == 1:
            attr_name = 'y'
        if axis == 2:
            attr_name = 'z'

        for i in range(0, len(positions)):
            state += f'{getattr(positions[i], attr_name)},{getattr(velocities[i], attr_name)},'

        return hash(state)

    step = 0
    axis_to_check = {0,1,2}
    axis_found = set()
    states_by_axis = [set(), set(), set()]
    periods = []

    while True:
        # debug output
        if step % 100000 == 0:
            print(f'{datetime.datetime.now().time()}: After {step} steps')

        if not axis_to_check:
            result = lcm.reduce(periods)
            print(f'Planets will return where they started after {result} steps')
            break

        for axis_i in axis_to_check:
            current_hash = axis_hash(positions, velocities, axis_i)
            if current_hash in states_by_axis[axis_i]:
                print(f'Repeat found for {axis_i} after {step} states')
                axis_found.add(axis_i)
                periods.append(step)
            else:
                states_by_axis[axis_i].add(current_hash)

        axis_to_check -= axis_found

        # update velocities
        for i in range(0, len(positions)):
            for j in range(0, len(positions)):
                # Don't compare with self
                if i == j:
                    continue

                delta_velocity = {
                    'x': velocity_update(positions[i].x, positions[j].x),
                    'y': velocity_update(positions[i].y, positions[j].y),
                    'z': velocity_update(positions[i].z, positions[j].z),
                }
                velocities[i] += Vector(**delta_velocity)

        # update positions
        for i in range(0, len(positions)):
            positions[i] += velocities[i]

        step += 1

