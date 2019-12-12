
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

    def total_energy(positions, velocities):
        total = 0
        for i in range(0, len(positions)):
            total += positions[i].energy * velocities[i].energy
        return total

    step = 0
    step_limit = 1000

    while step <= step_limit:
        # debug output
        if step % 100 == 0:
            print(f'After {step} steps')
            for i in range(0, len(positions)):
                print(f'pos={positions[i]}, vel={velocities[i]}')

            print(f'Sum of total energy: {total_energy(positions, velocities)}')

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

