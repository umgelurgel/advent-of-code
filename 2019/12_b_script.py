
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
    with open("12_input_test.txt","r") as file:
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

    def total_energy(positions, velocities):
        total = 0
        for i in range(0, len(positions)):
            total += positions[i].energy * velocities[i].energy
        return total

    def state_hash(positions, velocities):
        state = ''
        for i in range(0, len(positions)):
            state += f'{positions[i]},{velocities[i]},'

        return hash(state)

    def list_hash(planets):
        state = ''
        for i in range(0, len(planets)):
            state += f'{planets[i]},'

        return hash(state)

    step = 0
    states = set()
    pos_set = set()
    vel_set = set()

    while True:
        # debug output
        if step % 10000 == 0:
            print(f'After {step} steps')
            # for i in range(0, len(positions)):
            #     print(f'pos={positions[i]}, vel={velocities[i]}')
            # print(f'Sum of total energy: {total_energy(positions, velocities)}')

        pos_hash = list_hash(positions)
        if pos_hash in pos_set:
            print(f'Position repeat found after {step} states')
            for i in range(0, len(positions)):
                print(f'pos={positions[i]}, vel={velocities[i]}')
        else:
            pos_set.add(pos_hash)

        vel_hash = list_hash(velocities)
        if vel_hash in vel_set:
            print(f'Velocity repeat found after {step} states')
            for i in range(0, len(positions)):
                print(f'pos={positions[i]}, vel={velocities[i]}')
        else:
            vel_set.add(vel_hash)



        current_hash = state_hash(positions, velocities)
        if current_hash in states:
            print(f'Repeat found after {step} states')
            for i in range(0, len(positions)):
                print(f'pos={positions[i]}, vel={velocities[i]}')

            break
        else:
            states.add(current_hash)

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

